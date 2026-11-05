import requests

from sqlalchemy import text
from ..infra.database import get_db


def dump_database():
    db_generator = get_db()
    db = next(db_generator)

    try:
        # Récupération des associations
        response = requests.get("https://cal.minet.net/api/organizations", timeout=30)
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
            response = requests.get(
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
                    email = full_name.replace(" ", ".") + "@telecom-sudparis.eu"
                else:
                    full_name = ""

                # Insertion de l'utilisateur
                db.execute(
                    text("""
                        INSERT INTO users (
                            email,
                            first_name,
                            last_name,
                            is_admin
                        )
                        VALUES (
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
                    SELECT id FROM users WHERE email=:email
                    """),
                    {
                        "email": email,
                    },
                )
                db.execute(
                    text("""
                        INSERT INTO permission (
                            asso_id,
                            user_id
                        )
                        VALUES (
                            :asso_id,
                            :user_id
                        )
                        ON CONFLICT DO NOTHING; 
                    """),
                    {
                        "asso_id": asso_id,
                        "user_id": user_data.scalar_one(),
                    },
                )

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
