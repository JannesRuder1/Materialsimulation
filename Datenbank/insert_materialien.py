import sqlite3
import json

conn = sqlite3.connect("material_database.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS material_matrices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_name TEXT,
    matrix_data TEXT
)
""")

materials = [
    ("Lithium_tantalate", json.dumps({
        "youngs_modulus_GPa": 97.5,   # (125 + 70) / 2
        "youngs_modulus_values_GPa": [125, 70],
        "p11": 0.08,
        "p12": 0.08,
        "poissons_ratio": 0.22,
        "wavelength": 0.5876,
        "refractive_index": 2.1874
    })),
    ("Quartz", json.dumps({
        "youngs_modulus_GPa": 69.5,   # (99 + 40) / 2
        "youngs_modulus_values_GPa": [99, 40],
        "p11": 0.16,
        "p12": 0.27,
        "poissons_ratio": 0.17,
        "wavelength": 0.5876,
        "refractive_index": 1.4585
    })),
    ("Tellurium_dioxide", json.dumps({
        "youngs_modulus_GPa": 60,
        "youngs_modulus_values_GPa": [60],
        "p11": 0.0074,
        "p12": 0.187,
        "poissons_ratio": 0.14,
        "wavelength": 0.5876,
        "refractive_index": 2.2749
    }))
]

cursor.executemany("""
INSERT INTO material_matrices (material_name, matrix_data)
VALUES (?, ?)
""", materials)

conn.commit()
conn.close()