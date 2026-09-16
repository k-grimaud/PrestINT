import sqlite3

connexion = sqlite3.connect("prestint.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT,
    prix REAL NOT NULL,
    secret INTEGER NOT NULL DEFAULT 0
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

curseur.executemany(
    "INSERT INTO produits (nom, description, prix, secret) VALUES (?, ?, ?, ?)",
    produits,
)

connexion.commit()
connexion.close()

print("Base de données créée avec succès.")
