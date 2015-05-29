__author__ = 'Zhi Deng'

from pyqe.qe_input import get_template, write_input
from monty.os import cd


H_sites = {'top': (0, 0),
           'bridge': (0.25, 0.25),
           'hollow1': (0.33333, 0.16667),
           'hollow2': (0.16667, 0.33333)}

temp = get_template('Al.111.adsor')
with cd('scratch'):
    for k,v in H_sites.items():
        p = {'site': k, 'h_coords': '%s %s' % tuple(v)}
        write_input(temp, p, ['site'])