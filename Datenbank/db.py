import sqlite3

# Verbindung zur lokalen Datenbank herstellen
conn = sqlite3.connect("material_berechnung.db")
cursor = conn.cursor()

# Fremdschlüssel-Unterstützung in SQLite aktivieren
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Tabelle für die materialabhängigen Daten (Matrix) erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS material_matrizen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_name TEXT NOT NULL UNIQUE,
    matrix_daten TEXT NOT NULL           -- Hier kannst du deine Matrix (z.B. als JSON oder Text) speichern
)
""")


conn.commit()
print("Datenbank und Tabellen wurden erfolgreich erstellt!")
conn.close()