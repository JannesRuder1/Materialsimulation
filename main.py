import numpy as np
import math
import json
import sqlite3
import os


def P(length):
    return 1e3 * (1 + 0.01 * length)

def N(length):
    return 100 * (1 - 0.005 * length)

def T(length):
    return 10 * (1 + 0.01 * length)


def main():

    os.makedirs("Outputs", exist_ok=True)

    conn = sqlite3.connect("Datenbank/material_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM material_matrices")
    rows = cursor.fetchall()

    # 🔥 30 Werte
    length_values = np.linspace(0.5, 0.6, 30)

    # 🔥 Faktoren so gewählt, dass exakt ~1500 entsteht
    P_factors = np.linspace(0.85, 1.15, 5)
    N_factors = np.linspace(0.90, 1.10, 5)
    T_factors = np.linspace(0.95, 1.05, 2)

    for zeile in rows:

        daten = json.loads(zeile[2])
        material = zeile[1]

        n = float(daten["refractive_index"])
        wavelength = float(daten["wavelength"])
        E = float(daten["youngs_modulus_GPa"]) * 1e9
        nu = float(daten["poissons_ratio"])
        p11 = float(daten["p11"])
        p12 = float(daten["p12"])

        results = []

        K_pressure = (
            (2 * math.pi * n) / E
            * wavelength
            * (
                2 * nu
                + 0.5 * n**2
                * (p12 * (1 - 3 * nu) + p11 * (1 - nu))
            )
        )

        K_tension = (
            (2 * math.pi * n) / E
            * wavelength
            * (
                1
                - 0.5 * n**2
                * (p12 * (1 - nu) - nu * p11)
            )
        )

        K_torsion = (
            (math.pi * n) / (2 * wavelength * E)
            * (n**2 * (1 + nu) * (p11 - p12))
        )

        # 🔥 exakt 1500 Kombinationen
        for length in length_values:

            base_P = P(length)
            base_N = N(length)
            base_T = T(length)

            for fP in P_factors:
                for fN in N_factors:
                    for fT in T_factors:

                        P_val = base_P * fP
                        N_val = base_N * fN
                        T_val = base_T * fT

                        results.append({
                            "material": material,
                            "length": round(length, 4),
                            "P": P_val,
                            "N": N_val,
                            "T": T_val,
                            "factors": {
                                "P": round(fP, 3),
                                "N": round(fN, 3),
                                "T": round(fT, 3)
                            },
                            "delta_phi_pressure": K_pressure * P_val,
                            "delta_phi_tension": K_tension * N_val,
                            "delta_phi_torsion": K_torsion * T_val
                        })

        file = f"Outputs/simulation_{material}.json"

        results.sort(key=lambda x: (
    abs(x["delta_phi_pressure"]) +
    abs(x["delta_phi_tension"]) +
    abs(x["delta_phi_torsion"])
))

        with open(file, "w") as f:
            json.dump(results, f, indent=4)

        print("gespeichert:", file, "→", len(results), "Einträge")

    conn.close()


if __name__ == "__main__":
    main()