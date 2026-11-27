import re
import unicodedata

import requests
from requests.adapters import HTTPAdapter
from sqlalchemy import text
from urllib3.util import Retry

from ..infra.database import get_db


def dump_database():
    db_generator = get_db()
    db = next(db_generator)
    session = requests.Session()
    session.mount(
        "https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1))
    )  # retrying when a connection drops

    try:
        # Récupération des associations
        response = session.get("https://cal.minet.net/api/organizations", timeout=30)
        response.raise_for_status()

        list_association = response.json()

        for association in list_association:
            asso_id = association["id"]
            asso_name = association["name"]
            status = association["type"]

            # Insertion de l'association
            db.execute(
                text("""
                    INSERT INTO association (asso_id, name, status)
                    VALUES (:asso_id, :name, :status)
                    ON CONFLICT (asso_id) DO NOTHING
                """),
                {"asso_id": asso_id, "name": asso_name, "status": status},
            )

            # Récupération des membres
            response = session.get(
                f"https://cal.minet.net/api/organizations/{asso_id}/members", timeout=30
            )
            response.raise_for_status()

            list_user_association = response.json()

            for user in list_user_association:
                if user["full_name"]:
                    full_name = user["full_name"].strip().lower()
                    name_parts = full_name.split()
                    first_name = name_parts[0]
                    last_name = " ".join(name_parts[1:])
                    ascii_name = (
                        unicodedata.normalize("NFKD", full_name)
                        .encode("ascii", "ignore")
                        .decode()
                    )
                    email = (
                        re.sub(r"[^a-z0-9.-]", "", ascii_name.replace(" ", "."))
                        + "@telecom-sudparis.eu"
                    )
                else:
                    continue

                # Insertion de l'utilisateur
                db.execute(
                    text("""
                        INSERT INTO users (
                            user_id,
                            email,
                            first_name,
                            last_name,
                            is_admin
                        )
                        VALUES (
                            gen_random_uuid(),
                            :email,
                            :first_name,
                            :last_name,
                            :is_admin
                        )
                        ON CONFLICT (email) DO NOTHING;
                    """),
                    {
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "is_admin": False,
                    },
                )
                user_data = db.execute(
                    text("""
                    SELECT user_id FROM users WHERE email=:email
                    """),
                    {
                        "email": email,
                    },
                )
                db.execute(
                    text("""
                        INSERT INTO permission (
                            asso_id,
                            user_id,
                            permission
                        )
                        VALUES (
                            :asso_id,
                            :user_id,
                            :user_role
                        )
                        ON CONFLICT (asso_id, user_id) DO UPDATE SET permission = EXCLUDED.permission;
                    """),
                    {
                        "asso_id": asso_id,
                        "user_id": user_data.scalar_one(),
                        "user_role": user["role"],
                    },
                )

        db.execute(text("""
            INSERT INTO list_service (
                asso_id, name, approximative_cost,
                approximative_time, description, path
            )
            SELECT
                a.asso_id,
                'Tireuse mobile',
                25,
                '3 jours',
                'Location et mise en place de tireuse mobile (prix de la livraison en supplément)',
                ''
            FROM association a
            WHERE a.asso_id = '191c1827-d591-4338-9275-4054e3b93803'
            AND NOT EXISTS (
                SELECT 1 FROM list_service s
                WHERE s.asso_id = a.asso_id AND s.name = 'Tireuse mobile'
            )
        """))

        # Validation des insertions
        db.commit()

        print("Import des associations et utilisateurs terminé !")

    except Exception as e:
        db.rollback()
        print(f"Erreur lors de l'import : {e}")
        raise

    finally:
        db.close()
        db_generator.close()


if __name__ == "__main__":
    dump_database()
