"""
.. module:: MusicFiles

MusicFiles
*************

:Description: MusicFiles

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2014 14:01 

"""

__author__ = 'bejar'

import scipy.io
import numpy as np
from util.paths import cpath, rpath
from operator import itemgetter, attrgetter, methodcaller



def cluster_times(nexp, clpeaks, timepeaks, nfile, remap):

    # Select the index of the experiment
    peakini = 0
    i = 0
    while i < nexp:
        exp = timepeaks[i]
        peakini += exp.shape[0]
        i += 1

    exp = timepeaks[nexp]
    peakend = peakini + exp.shape[0]

    # Build the sequence string
    peakstr = []

    print exp.shape, peakini, peakend
    for i in range(peakini, peakend):
        peakstr.append([remap[clpeaks[i][0]-1],exp[i-peakini][0]])

    return peakstr




def generate_sequences():
    clstfreq = {}

    for i in range(0, timepeaks[0].shape[0]):
        if clpeaks[i][0] in clstfreq:
            clstfreq[clpeaks[i][0]] += 1
        else:
            clstfreq[clpeaks[i][0]] = 1

    lclstfreq = [(k, clstfreq[k]) for k in clstfreq]
    lclstfreq = sorted(lclstfreq, key=itemgetter(1), reverse=True)
    remap = [i for i, _ in lclstfreq]

    data = {}
    for exp, nfile in nfiles:
        peaklist = cluster_times(exp, clpeaks, timepeaks, line+'-'+nfile, remap)
        data['E{0:0>2d}{1}'.format(exp, nfile)] = np.array(peaklist)
    return data


nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
          (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
          ]

# nfiles = [(0, 'ctrl1'), (1, 'ctrl2')]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'



aline = [('L4cd', 'k9.n5', 9),
         ('L4ci', 'k9.n1', 9),
        ('L5cd', 'k10.n6' , 10),
        #('L5rd', 'k20.n1' ),
        ('L5ci', 'k15.n1', 15),
        ('L5ri', 'k15.n9', 15),
        ('L6cd', 'k17.n1', 17),
        ('L6rd', 'k13.n9', 13),
        #('L6ci', 'k15.n1'),
        ('L6ri', 'k18.n4', 18),
        ('L7ri', 'k18.n4', 18)
        ]

# aline = [('L6cd', 'k17.n1'),
#         ('L6ci', 'k15.n1')
#         ]


for line,clust,_ in aline:
    matpeaks = scipy.io.loadmat( cpath + '/Selected/centers.' + line + '.' + clust + '.mat')
    mattime = scipy.io.loadmat( cpath + '/WholeTime.' + line + '.mat')

    clpeaks = matpeaks['IDX']
    timepeaks = mattime['temps'][0]
    peakdata = generate_sequences()

    scipy.io.savemat(rpath+'peaks-'+line,peakdata)
    print '--------------------'

