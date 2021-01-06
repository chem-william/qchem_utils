import os
import numpy as np
from ase.io import read
from ase.units import _c as light_speed
from ase.units import J
from ase.units import _Nav

bohr_radius = 5.29e-11  # m
bohr_radius = 5.29e-11*1000  # cm

_dalton = 1.66053906660e-27

with open("./h2o.log") as log_file:
    lines = log_file.readlines()

    # Get number of atoms
    num_atoms = 0
    for idx, line in enumerate(lines):
        if "NAtoms=" in line:
            line = line.split()
            num_atoms = int(line[1])
    amount_constants = 3*num_atoms

    force_constants_bookmark = 0
    for idx, line in enumerate(lines[::-1]):
        if "Force constants in Cartesian coordinates" in line:
            force_constants_bookmark = idx
            break

    force_idx = 0
    extracted_force = []
    flag = False
    for idx, line in enumerate(lines[-force_constants_bookmark - 1:]):
        if "FormGI is forming the generalized" in line:
            break

        if "Force constants in Cartesian coordinates" in line:
            flag = True
            continue

        if flag:
            extracted_force.append(line)

    tmp_matrix = []
    for idx, line in enumerate(extracted_force[1:]):
        line = line.split()[1:]
        line = [float(x.replace("D", "e")) for x in line]
        if idx != 0 and idx % 9 == 0:
            continue
        for entry in line:
            tmp_matrix.append(entry)
    tmp_matrix = np.array(tmp_matrix, dtype="float64").ravel()

    force_constants = np.zeros((amount_constants, amount_constants))
    count = 0
    for idx in range(1, amount_constants + 1):
        force_constants[idx - 1, :idx] = tmp_matrix[count:count + idx]
        count += idx
    print(force_constants)
    ofiwjeofij
    force_constants += np.tril(force_constants, -1).T

    for row in force_constants:
        print(row.sum())

    mol = read("./h2o.xyz")

    masses = mol.get_masses()
    rminv = (masses**-.5).repeat(3)
    dynamical = force_constants * rminv[:, None] * rminv[None, :]

    vals, vecs = np.linalg.eigh(dynamical)

    # print(np.sqrt(vals)*220000)
    # print(np.sqrt(vals/(4*np.pi**2*light_speed**2)))
