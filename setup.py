__author__ = 'Zhi Deng'

import os
from setuptools import setup, find_packages

module_dir = os.path.dirname(os.path.abspath(__file__))
setup(
    name = "pyqe",
    version = "0.1",
    packages = find_packages(),
    install_requires=['numpy','pandas','monty','pymatgen'],
    scripts = [os.path.join('scripts', f) for f in
               os.listdir(os.path.join(module_dir, 'scripts'))]
)