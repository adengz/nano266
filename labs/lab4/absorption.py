__author__ = 'Zhi Deng'

from pyqe.qe_input import get_template, write_input
from monty.os import cd


H_sites = {'top': (0, 0, 0.05),
           'bridge': (0.25, 0.25, 0.04),
           'hollow1': (0.33333, 0.16667, 0.03),
           'hollow2': (0.16667, 0.33333, 0.03)}

temp = get_template('AlH.111.absor')
with cd('scratch'):
    for k,v in H_sites.items():
        p = {'site': k, 'h_coords': '%s %s %s' % tuple(v)}
        write_input(temp, p, ['site'])
