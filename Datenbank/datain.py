import sqlite3

conn = sqlite3.connect("material_berechnung.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# A) Materialien mit ihren Matrizen hinzufügen
materialien = [
    ("Aluminium-Verbund", "[[1.1, 0.2], [0.2, 1.1]]"),
    ("Kohlefaser-Matrix", "[[2.5, 0.1], [0.1, 2.5]]")
]

cursor.executemany("""
INSERT OR IGNORE INTO material_matrizen (material_name, matrix_daten)
VALUES (?, ?)
""", materialien)


# B) Berechnungen hinzufügen (Die Zahlen am Ende stehen für die material_id)
# 1 = Aluminium, 2 = Kohlefaser
projekte = [
    ("Simulation_A", 150.5, 632.8, 1), 
    ("Simulation_B", 200.0, 532.0, 1),
    ("Test_Projekt_C", 75.2, 1064.0, 2)
]

cursor.executemany("""
INSERT INTO berechnungen (berechnungs_name, laenge, wellenlaenge, material_id)
VALUES (?, ?, ?, ?)
""", projekte)

conn.commit()
print("Testdaten erfolgreich eingefügt!")
conn.close()
