import os
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

output_dir = "Outputs"

def get_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def plot_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    if not data:
        return
    lengths = [entry['length'] for entry in data]
    delta_phi_pressure = [entry['delta_phi_pressure'] for entry in data]
    delta_phi_tension = [entry['delta_phi_tension'] for entry in data]
    delta_phi_torsion = [entry['delta_phi_torsion'] for entry in data]
    material = data[0]['material'] if 'material' in data[0] else os.path.basename(filepath)

    # 1. 2D-Plot: delta_phi_tension (N) vs. length
    plt.figure(figsize=(8,5))
    plt.plot(lengths, delta_phi_tension, label='delta_phi_tension (N)', color='blue')
    plt.xlabel('Length')
    plt.ylabel('delta_phi_tension')
    plt.title(f'delta_phi_tension (N) für {material}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"plot_{material}_N.png"))
    plt.close()

    # 2. 3D-Plot: delta_phi_tension (N), delta_phi_torsion (T) vs. length
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(lengths, delta_phi_tension, delta_phi_torsion, label='N,T')
    ax.set_xlabel('Length')
    ax.set_ylabel('delta_phi_tension (N)')
    ax.set_zlabel('delta_phi_torsion (T)')
    ax.set_title(f'3D-Plot N,T für {material}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"plot_{material}_NT_3D.png"))
    plt.close()

    # 3. 2D-Plot: (N+T) vs. length
    sum_NT = np.array(delta_phi_tension) + np.array(delta_phi_torsion)
    plt.figure(figsize=(8,5))
    plt.plot(lengths, sum_NT, label='delta_phi_tension + delta_phi_torsion', color='green')
    plt.xlabel('Length')
    plt.ylabel('delta_phi_N + delta_phi_T')
    plt.title(f'delta_phi_N + delta_phi_T für {material}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"plot_{material}_NplusT.png"))
    plt.close()

    # 4. 2D-Plot: (N+T+P) vs. length
    sum_NTP = np.array(delta_phi_tension) + np.array(delta_phi_torsion) + np.array(delta_phi_pressure)
    plt.figure(figsize=(8,5))
    plt.plot(lengths, sum_NTP, label='N+T+P', color='red')
    plt.xlabel('Length')
    plt.ylabel('delta_phi_N + delta_phi_T + delta_phi_P')
    plt.title(f'delta_phi_N + delta_phi_T + delta_phi_P für {material}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"plot_{material}_NplusTplusP.png"))
    plt.close()

    print(f"Plots für {material} gespeichert.")

if __name__ == "__main__":
    json_files = get_json_files(output_dir)
    for json_file in json_files:
        plot_json_file(os.path.join(output_dir, json_file))
