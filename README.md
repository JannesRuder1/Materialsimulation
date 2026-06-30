# Materialsimulation

Dieses Projekt simuliert verschiedene Materialeigenschaften und berechnet resultierende Werte für Druck, Zug und Torsion. Die Ergebnisse werden als JSON-Dateien gespeichert.

## Hauptfunktionen
- Liest Materialdaten aus einer SQLite-Datenbank (`material_database.db`).
- Führt für verschiedene Längen und Faktoren Simulationen durch.
- Berechnet delta_phi für Druck, Zug und Torsion.
- Speichert die Ergebnisse sortiert als JSON-Dateien im Ordner `Outputs`.
- Optimiert für Performance durch parallele Verarbeitung.

## Nutzung
1. Stelle sicher, dass die Datenbank `material_database.db` im Ordner `Datenbank` existiert und die Tabelle `material_matrices` enthält.
2. Starte das Skript mit:
   ```
   python main.py
   ```
3. Die Ergebnisse werden im Ordner `Outputs` als `simulation_<Materialname>.json` gespeichert.

## Abhängigkeiten
- numpy
- math
- json
- sqlite3
- os
- concurrent.futures

Installiere fehlende Pakete ggf. mit pip:
```
pip install numpy
```

## Anpassung
Passe die Funktionen `P`, `N`, `T` oder die Wertebereiche in `main.py` nach Bedarf an.

