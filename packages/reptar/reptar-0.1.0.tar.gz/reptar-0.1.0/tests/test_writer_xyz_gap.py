# MIT License
#
# Copyright (c) 2022-2023, Alex M. Maldonado
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests writing XYZ files for GAP code"""

# pylint: skip-file

import sys
import os
import pytest
import numpy as np
from reptar import File
from reptar.writers import write_xyz_gap

sys.path.append("..")

# Ensures we execute from file directory (for relative paths).
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Source paths
DATA_DIR = "./data/"

# Writing paths
WRITING_DIR = "./tmp/writing/"
os.makedirs(WRITING_DIR, exist_ok=True)


def test_xyz_gap_writer_1h2o_120meoh_prod():
    r"""Writing short XYZ file from exdir file"""
    exdir_path = os.path.join(DATA_DIR, "1h2o_120meoh_md.exdir")
    xyz_path = os.path.join(WRITING_DIR, "1h2o_120meoh_md_gap.xyz")

    rfile = File(exdir_path, mode="r")

    lattice = np.array([[200.0, 0.0, 0.0], [0.0, 200.0, 0.0], [0.0, 0.0, 200.0]])
    Z = rfile.get("eq_1/atomic_numbers")
    R = rfile.get("eq_1/geometry")[:5]
    E = rfile.get("eq_1/energy_pot")[:5]  # Hartree
    E *= 27.21138602  # eV
    write_xyz_gap(xyz_path, lattice, Z, R, E)

    # TODO: Write tests
