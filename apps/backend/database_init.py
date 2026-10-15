import sqlite3

connexion = sqlite3.connect("prestint.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mail VARCHAR(50) UNIQUE,
    password_hashed VARCHAR(500),
    category VARCHAR(20)
)
""")

produits = [
    (
        "Ruban décoloré",
        "Si tu est mignon, les monstres ne te frapperont pas aussi fort",
        1000,
        0,
    ),
    ("Masque Sheikah", "Il ressemble à un masque en tissu ordinaire...", 5000.00, 0),
    (
        "Grosses bottes",
        "Une paire de bottes robustes qui protège le porteur des pièges tendus sur le terrain",
        200000,
        0,
    ),
]

# curseur.executemany(
#     "INSERT INTO produits (nom, description, prix, secret) VALUES (?, ?, ?, ?)",
#     produits,
# )

connexion.commit()
connexion.close()

print("Base de données créée avec succès.")
