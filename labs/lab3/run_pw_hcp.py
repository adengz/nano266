#!/usr/bin/env python

"""
This is a very simple python starter script to automate a series of PWSCF
calculations. If you don't know Python, get a quick primer from the official
Python documentation at https://docs.python.org/2.7/. The script is deliberately
simple so that only basic Python syntax is used and you can get comfortable with
making changes and writing programs.

Author: Shyue Ping Ong
"""

import os
import shutil
import numpy as np

# Load the Si.pw.in.template file as a template.
with open("Fe.hcp.pw.in.template") as f:
    template = f.read()

# Set default values for various parameters
#k = 8 # k-point grid of 8x8x8
alat = 5.42 # The lattice parameter for the cell in Bohr.
calat = 1.73
k1_array = np.arange(4,17)
k3_array = np.ceil(k1_array/calat)

# Loop through different k-points.
for k1,k3 in zip(k1_array,k3_array):
    # This generates a string from the template with the parameters replaced
    # by the specified values.
    s = template.format(alat=alat, calat=calat, k1=k1, k3=k3)

    # Let's define an easy jobname.
    jobname = "Fe_hcp_%s_%s" % (alat, k1)

    # Write the actual input file for PWSCF.
    with open("%s.pw.in" % jobname, "w") as f:
        f.write(s)

    #Print some status messages.
    print("Running with alat = %s, k = %s..." % (alat, k1))
    # Run PWSCF. Modify the pw.x command accordingly if needed.
    os.system("pw.x -inp {jobname}.pw.in > {jobname}.out".format(jobname=jobname))

    print("Done. Output file is %s.out." % jobname)

# This just does cleanup. For this lab, we don't need the files that are
# dumped into the tmp directory.
shutil.rmtree("tmp")
