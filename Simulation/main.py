import numpy as np
import math
import json


def main():

    output = []

    # Matrix für SiO₂
    Pij = [[0.16, 0.27 , 0,27], 
           [0.27, 0.16, 0.27],
           [0.27, 0.27, 0.16]]

    # Einheitsvektoren x,y und z
    E1 = np.array([1, 0, 0])
    E2 = np.array([0, 1, 0])
    E3 = np.array([0, 0, 1])

    # wavelength of visible light in meters
    wavelength = 0.005876

    # length of the cable in meters
    min_length = 0.5
    max_length = 1
    
    # refractive index from the fiber (SiO₂)
    refractive_Index = 1.4585

    last_length = min_length

    while last_length < max_length:
        length = last_length
        first_part = (2 * math.pi * length) / wavelength
        second_part = (refractive_Index ** 2) / 2 * (Pij[0][0] * E2) + (Pij[0][1]*(E1 + E3))
        result = first_part * second_part
        print(result)
        last_length += 0.001

        output.append(result.tolist())

    with open("output.json", "w") as file:
        json.dump(list(output), file, indent=4)
        

    





    print(result)




    
    


main()