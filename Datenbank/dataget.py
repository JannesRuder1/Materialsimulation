import sqlite3

conn = sqlite3.connect("material_berechnung.db")
cursor = conn.cursor()

# Abfrage über beide Tabellen hinweg
query = """
SELECT 
    b.berechnungs_name, 
    b.laenge, 
    b.wellenlaenge, 
    m.material_name, 
    m.matrix_daten
FROM berechnungen b
JOIN material_matrizen m ON b.material_id = m.id
"""

cursor.execute(query)
ergebnisse = cursor.fetchall()

print(f"{'Berechnung':<15} | {'Länge':<6} | {'Welle':<6} | {'Material':<18} | Matrix")
print("-" * 75)

for reihe in ergebnisse:
    print(f"{reihe[0]:<15} | {reihe[1]:<6} | {reihe[2]:<6} | {reihe[3]:<18} | {reihe[4]}")

conn.close()