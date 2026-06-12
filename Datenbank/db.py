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

# 2. Tabelle für die unabhängigen Daten erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS berechnungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Material_name TEXT NOT NULL,
    p11 REAL NOT NULL,               
    p12 REAL NOT NULL,
    p13 REAL NOT NULL,
    p14 REAL NOT NULL,
    p31 REAL NOT NULL,
    p33 REAL NOT NULL,
    p41 REAL NOT NULL,
    p44 REAL NOT NULL,          
    material_id INTEGER,                 -- Verknüpfung zum Material
    FOREIGN KEY (material_id) REFERENCES material_matrizen(id)
)
""")

conn.commit()
print("Datenbank und Tabellen wurden erfolgreich erstellt!")
conn.close()