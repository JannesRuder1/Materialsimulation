import sqlite3
import json

conn = sqlite3.connect("material_berechnung.db")
cursor = conn.cursor()

materialen = [
    ("Lithium_niobate", json.dumps({"p11": 0.08, "p12": 0.08})),
    ("Quartz", json.dumps({"p11": 0.16, "p12": 0.27})),
    ("Tellurium_dioxide", json.dumps({"p11": 0.0074, "p12": 0.187})),
    ("KDP", json.dumps({"p11": 0.251, "p12": 0.249}))
]

cursor.executemany("""
INSERT INTO material_matrizen (material_name, matrix_daten)
VALUES (?, ?)
""", materialen)

conn.commit()
conn.close()