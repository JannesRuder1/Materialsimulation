import numpy as np
import math
import json
import sqlite3
import os


def P(z):
    return 1e3 * (1 + 0.01 * z)

def N(z):
    return 100 * (1 - 0.005 * z)

def T(z):
    return 10 * (1 + 0.01 * z)


def main():

    os.makedirs("Outputs", exist_ok=True)

    conn = sqlite3.connect("Datenbank/material_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM material_matrices")
    rows = cursor.fetchall()

    step = 0.001

    for zeile in rows:

        daten = json.loads(zeile[2])
        material = zeile[1]

        n = float(daten["refractive_index"])
        wavelength = float(daten["wavelength"])
        E = float(daten["youngs_modulus_GPa"]) * 1e9
        nu = float(daten["poissons_ratio"])
        p11 = float(daten["p11"])
        p12 = float(daten["p12"])

        # stabilere Werte als arange
        z_values = np.linspace(0.5, 0.6, int((0.6 - 0.5) / step) + 1)

        results = []

        for z in z_values:

            P_val = P(z)
            N_val = N(z)
            T_val = T(z)

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

            result = {
                "material": material,
                "z": round(z, 4),
                "P": P_val,
                "N": N_val,
                "T": T_val,
                "delta_phi_pressure": K_pressure * P_val,
                "delta_phi_tension": K_tension * N_val,
                "delta_phi_torsion": K_torsion * T_val
            }

            results.append(result)

        file = f"Outputs/simulation_{material}.json"

        with open(file, "w") as f:
            json.dump(results, f, indent=4)

        print("gespeichert:", file)

    conn.close()


if __name__ == "__main__":
    main()