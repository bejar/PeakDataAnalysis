"""
.. module:: GenerateSequences

GenerateSequences
*************

:Description: GenerateSequences

    

:Authors: bejar
    

:Version: 

:Created on: 02/10/2014 13:22 

"""

__author__ = 'bejar'


import scipy.io
import numpy as np


def compute_delta(nfiles, timepeaks):
    for i,name in nfiles:
        exp = timepeaks[i]
        ldelta = []
        for i in range(exp.shape[0]-1):
            ldelta.append(0.6*(exp[i+1]-exp[i]))

        np.savetxt(rpath + 'delta' + name + '.csv', np.array(ldelta), fmt='%f')


cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/'
rpath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/'

nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
          (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
          ]

#matpeaks = scipy.io.loadmat( cpath+'/centers.L6ri.k15.n3.mat')
mattime = scipy.io.loadmat(cpath+'/WholeTime.L6ri.mat')

#clpeaks = matpeaks['IDX']
timepeaks = mattime['temps'][0]

#print clpeaks.shape
print timepeaks.shape

# s = 0
# for i in range(timepeaks.shape[0]):
#     print timepeaks[i].shape[0]
#     s += timepeaks[i].shape[0]
# print s

compute_delta(nfiles, timepeaks)






