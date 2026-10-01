"""
Module for authenticating users by email.
The user enters their email address (which must be of the form prenom.nom@telecom-sudparis.eu) and then receives an email containing the OTP.
"""


import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from authentification.otp import OTP_TTL


log = logging.getLogger(__name__)

_env = Environment(
    undefined=StrictUndefined,
    autoescape=True,
    loader=FileSystemLoader(Path(__file__).parent / "template")
)

def send_otp_mail(destination: str, code: str) -> None:
    """
    Sends the OTP to destination; logs it instead when OTP_DEV_LOG is set and no SMTP_HOST.
    """

    host = os.getenv("SMTP_HOST")

    if not host:
        if os.getenv("OTP_DEV_LOG"): # OTP will be prompted IN PLAIN TEXT !!
            log.warning("DEV ONLY PURPOSES - OTP for %s: %s", destination, code)
            return

        raise RuntimeError("no SMTP_HOST set - check your .env file")

    ttl = int(OTP_TTL.total_seconds() // 60) # TTL in minutes
    msg = EmailMessage()
    msg["Subject"] = "Code de connexion Prest'INT"
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = destination
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    msg.set_content( # For client without HTML
        f"Code de connexion Prest'INT: {code}\nIl expire dans {ttl} minutes\n\nVous n'êtes pas à l'origine de cette tentative de connexion? Aucune fonctionnalité n'est prévu pour le moment :ç"
    )
    msg.add_alternative(
        _env.get_template("otp.html").render(
            code=code,
            email=destination,
            ttl_min=ttl,
            base_url=os.getenv("BASE_URL", "http://localhost:5173")
        ),
        subtype="html"
    )

    port = int(os.getenv("SMTP_PORT", "587"))
    context = ssl.create_default_context()

    try:
        smtp = smtplib.SMTP_SSL(host, port, timeout=10, context=context) if port == 465 else smtplib.SMTP(host, port, timeout=10)

        with smtp as s:
            if port == 587:
                s.starttls(context=context)

            if user := os.getenv("SMTP_USER"):
                s.login(user, os.environ["SMTP_PASSWORD"])

            s.send_message(msg)
    except (smtplib.SMTPException, OSError):
        log.exception("Couldn't send an OTP mail to %s", destination)
