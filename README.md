# Material Simulation (Photoelasticity / Faser-Modell)

## Überblick

Dieses Projekt simuliert die optische Phasenverschiebung in einem Material entlang einer 1D-Strecke z ∈ [0.5, 0.6].

Es wird ein vereinfachtes physikalisches Modell verwendet, das mechanische Belastungen (Druck, Zug, Torsion) in optische Phasenänderungen (Photoelastizität) umrechnet.

Die Materialparameter werden aus einer SQLite-Datenbank geladen und für jedes Material separat ausgewertet.

---

# Installation

## Voraussetzungen
- Python 3.9+
- numpy

## Installation
```bash
pip install numpy
```

---

# Datenbankstruktur

Datei:
Datenbank/material_database.db

Tabelle:
material_matrices

Die Spalte zeile[2] enthält JSON-Daten:

{
  "refractive_index": 1.45,
  "wavelength": 1550e-9,
  "youngs_modulus_GPa": 70,
  "poissons_ratio": 0.17,
  "p11": 0.12,
  "p12": 0.27
}

---

# Physikalisches Modell

## Druck
P(z) = 10^3 * (1 + 0.01z)

## Zug
N(z) = 100 * (1 - 0.005z)

## Torsion
T(z) = 10 * (1 + 0.01z)

---

# Numerische Diskretisierung

z ∈ [0.5, 0.6], Δz = 0.001

---

# Ziel

- Simulation von Faseroptik-Sensoren
- Analyse von Belastung → Phasenverschiebung
- Vergleich verschiedener Materialien
