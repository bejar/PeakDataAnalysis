"""
.. module:: PeaksSynchro

PeaksSynchro
*************

:Description: PeaksSynchro

    

:Authors: bejar
    

:Version: 

:Created on: 19/11/2014 10:52 

"""

__author__ = 'bejar'

import scipy.io
import numpy as np
from util.paths import cpath, rpath
from operator import itemgetter, attrgetter, methodcaller


nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
          (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
          ]

# nfiles = [(0, 'ctrl1'), (1, 'ctrl2')]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# aline = [#('L4cd', 'k19.n1'),
#          ('L4ci', 'k20.n1'),
#         ('L5cd', 'k10.n1' ),
#         #('L5rd', 'k20.n1' ),
#         ('L5ci', 'k21.n1' ), ('L5ri', 'k20.n1' ),
#         ('L6cd', 'k17.n1'), ('L6rd', 'k20.n1'),
#         ('L6ci', 'k15.n1'),  ('L6ri', 'k18.n1'),
#         ('L7ri', 'k18.n1')
#         ]
aline = [('L6cd', 'k17.n1'),
        ('L6ci', 'k15.n1')
        ]


for line,clust in aline:
    matpeaks = scipy.io.loadmat( cpath + '/centers.' + line + '.' + clust + '.mat')
    mattime = scipy.io.loadmat( cpath + '/WholeTime.' + line + '.mat')

    clpeaks = matpeaks['IDX']
    timepeaks = mattime['temps'][0]
    peakdata = generate_sequences()

    scipy.io.savemat(rpath+'peaks-'+line,peakdata)
    print '--------------------'

