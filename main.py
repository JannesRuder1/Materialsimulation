import numpy as np
import math
import json
import sqlite3
import os
import concurrent.futures

def P_int(L):
    return 1000 * (L + 0.005 * L**2)

def N_int(L):
    return 100 * (L - 0.0025 * L**2)

def T_int(L):
    return 10 * (L + 0.005 * L**2)

def compute_result(args):
    (material, daten,
     K_pressure, K_tension, K_torsion,
     length, P_int_val, N_int_val, T_int_val,
     P_factors, N_factors, T_factors) = args

    local_results = []

    for fP in P_factors:
        for fN in N_factors:
            for fT in T_factors:

                P_val = P_int_val * fP
                N_val = N_int_val * fN
                T_val = T_int_val * fT

                local_results.append({
                    "material": material,
                    "length": round(length, 6),
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

    return local_results

def main():

    os.makedirs("Outputs", exist_ok=True)

    conn = sqlite3.connect("Datenbank/material_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM material_matrices")
    rows = cursor.fetchall()

    length_values = np.linspace(0.5, 0.51, 30)

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

        K_pressure = (
            (2 * math.pi * n) / (E * wavelength)
            * (
                2 * nu
                + 0.5 * n**2 * (
                    p11 * (1 - 3 * nu)
                    + p12 * (1 - nu)
                )
            )
        )

        K_tension = (
            (2 * math.pi * n) / (E * wavelength)
            * (
                1
                - 0.5 * n**2 * (
                    p12 * (1 - nu)
                    - nu * p11
                )
            )
        )

        K_torsion = (
            - (math.pi * n) / (2 * wavelength * E)
            * (n**2 * (1 + nu) * (p11 - p12))
        )

        args_list = []

        for length in length_values:

            P_int_val = P_int(length)
            N_int_val = N_int(length)
            T_int_val = T_int(length)

            args_list.append((
                material,
                daten,
                K_pressure,
                K_tension,
                K_torsion,
                length,
                P_int_val,
                N_int_val,
                T_int_val,
                P_factors,
                N_factors,
                T_factors
            ))

        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for local_results in executor.map(compute_result, args_list):
                results.extend(local_results)

        results.sort(key=lambda x: (
            abs(x["delta_phi_pressure"]) +
            abs(x["delta_phi_tension"]) +
            abs(x["delta_phi_torsion"])
        ))

        file = f"Outputs/simulation_{material}.json"

        with open(file, "w") as f:
            json.dump(results, f, indent=4)

        print("gespeichert:", file, "→", len(results), "Einträge")

    conn.close()

if __name__ == "__main__":
    main()