"""
"""


import os
import secrets
import hmac

from datetime import timedelta
from datetime import datetime
from datetime import timezone
from sqlalchemy import update, text, func, select

from infra.models.identity import Users
from infra.models.audit import OtpCode
from infra.models.audit import AuditEvent

OTP_LEN = 6
OTP_TTL = timedelta(minutes=5)
OTP_MAX_ATTEMPTS = 5
OTP_REQUESTS_PER_EMAIL = (3, timedelta(minutes=15))
OTP_REQUESTS_PER_IP = (20, timedelta(hours=1))
SESSION_TTL = timedelta(days=1)
OTP_SECRET = os.environ["OTP_SECRET"].encode() # make sure you set it up in the .env --> otherwise crash


def _fail(db, ip: str, email: str) -> None:
    """
    """

    audit(db, "login_fail", ip, detail={"email": email})
    db.commit()

    return None

def generate_otp_code() -> str:
    """
    Returns an n-digits OTP where n is defined by OTP_LEN
    """

    return f"{secrets.randbelow(10**OTP_LEN):0{OTP_LEN}d}"

def hash_email_otp(email: str, code: str) -> str:
    """
    Hashes the email OTP using OTP_SECRET (defined in .env) and sha256.
    Returns the hex representation of the hashed code
    """

    return hmac.new(OTP_SECRET, f"{email}:{code}".encode(), "sha256").hexdigest()

def hit_rate_limit(db, bucket: str, limit: int, window: timedelta) -> bool:
    """
    Returns true if the given bucket hit its rate limit
    """

    # Getting count and updating it with an atomic querry
    count = db.execute(
        text(
            """
            INSERT INTO rate_limits (bucket, count, expires_at) VALUES (:b, 1, now() + :w)
            ON CONFLICT (bucket) DO UPDATE SET
            count = CASE WHEN rate_limits.expires_at < now() THEN 1 ELSE rate_limits.count + 1 END,
            expires_at = CASE WHEN rate_limits.expires_at < now() THEN now() + :w ELSE rate_limits.expires_at END
            RETURNING count
            """
        ),
        {"b": bucket, "w": window}
    ).scalar_one()

    return count > limit

def request_otp(db, email: str, ip: str) -> str | None:
    """
    Returns the new code sent to the user email or None if rate limited
    """

    # Checking rate limits for IP and Email using two separate buckets
    # otp:email:{user_email} for email and otp:ip:{user_ip} for IP
    if hit_rate_limit(db, f"otp:email:{email}", *OTP_REQUESTS_PER_EMAIL) or hit_rate_limit(db, f"otp:ip:{ip}", *OTP_REQUESTS_PER_IP):
        audit(db, "otp_rate_limited", ip, detail={"email": email})
        db.commit()

        return None

    # Consumes the last OTP for the user's email
    db.execute(
        update(OtpCode).where(
            OtpCode.email==email, OtpCode.consumed_at.is_(None)
        ).values(consumed_at=func.now())
    )

    code = generate_otp_code()

    # Adding OTP code in the DB
    db.add(OtpCode(email=email, code_hash=hash_email_otp(email, code), expires_at=datetime.now(timezone.utc) + OTP_TTL))
    audit(db, "otp_sent", ip, detail={"email": email})

    db.commit()

    return code

def verify_otp(db, email: str, code: str, ip: str) -> Users | None:
    """
    Verifies if the user specified OTP matches that of the DB (hashed). It also handles attempt verifications.
    """

    row: OtpCode = db.scalars(select(OtpCode).where(OtpCode.email == email, OtpCode.consumed_at.is_(None), OtpCode.expires_at > func.now()).order_by(OtpCode.created_at.desc()).limit(1).with_for_update()).first()

    if row is None:
        return _fail(db, ip, email)

    row.attempts +=1

    if not hmac.compare_digest(row.code_hash, hash_email_otp(email, code)):
        if row.attempts >= OTP_MAX_ATTEMPTS:
            row.consumed_at = func.now() # User exceeded the number of miss allowed --> OTP is consumed

        return _fail(db, ip, email)

    row.consumed_at = func.now()
    user = get_user(db, email)
    audit(db, "login_ok", ip, user_id=user.user_id)
    db.commit()

    return user

def get_user(db, email: str) -> Users:
    """
    Side effect: creates a user in the DataBase if it does not exist at the time this function is called
    """

    user: Users =db.scalars(select(Users).where(Users.email == email)).first()

    first_name, last_name = email.split("@")[0].split(".")

    if not user:
        user = Users(email=email, first_name=first_name, last_name=last_name)
        db.add(user)
        db.flush()

    return user

def audit(db, event_type: str, ip: str, user_id=None, detail=None) -> None:
    """
    """

    db.add(AuditEvent(event_type=event_type, ip=ip, user_id=user_id, detail=detail))
