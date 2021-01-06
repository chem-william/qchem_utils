import os
import numpy as np
from ase.io import read
import matplotlib.pyplot as plt

with open("./hessian") as out_file:
    out_file.readline()

    lines = out_file.readlines()

    prev_atom_idx = 0
    forces = []
    tmp_forces = []
    for idx, line in enumerate(lines):
        if "$end" in line:
            forces.append(np.array(tmp_forces))
            tmp_forces = []
            break

        line = line.split()
        new_atom_idx = int(line[0])

        if prev_atom_idx == new_atom_idx or new_atom_idx == 1:
            for val in line[2:]:
                tmp_forces.append(float(val))
        else:
            forces.append(np.array(tmp_forces))

            tmp_forces = []
            for val in line[2:]:
                tmp_forces.append(float(val))
        prev_atom_idx = new_atom_idx
    forces = np.array(forces)

forces = forces[0::3, 0::3]
plt.imshow(forces, origin="lower")
plt.show()
np.save("./turbomole_force_constants.npy", forces)
