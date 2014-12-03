"""
.. module:: PeaksProcessModelling

PeaksProcessModelling
*************

:Description: PeaksProcessModelling

    

:Authors: bejar
    

:Version: 

:Created on: 28/11/2014 12:32 

"""

__author__ = 'bejar'

import operator
import scipy.io
import numpy as np
from pylab import *
from operator import itemgetter, attrgetter, methodcaller
from pypm.footprint import Alpha
from pypm.petri_net import PetriNet
import time
from util.XES import write_xes

def generate_log(nexp, clpeaks, timepeaks, remap, gap=0):
    """
    Secuencias con soporte mas que un limite grabadas en fichero de texto

    :param nexp:
    :param clpeaks:
    :param timepeaks:
    :param sup:
    :param nfile:
    :param remap:
    :param gap:
    :return:
    """
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
    peakset = []

    for i in range(peakini, peakend):
        peakset.append(voc[remap[clpeaks[i][0]-1]])
        if i < peakend-1 and gap != 0:
            if (timepeaks[nexp][i-peakini+1] - timepeaks[nexp][i-peakini]) > gap:
                peakstr.append(peakset)
                peakset = []

    return peakstr

def generate_model_log(line):
    clstfreq = {}

    for i in range(0, timepeaks[0].shape[0]):
        if clpeaks[i][0] in clstfreq:
            clstfreq[clpeaks[i][0]] += 1
        else:
            clstfreq[clpeaks[i][0]] = 1

    lclstfreq = [(k, clstfreq[k]) for k in clstfreq]
    lclstfreq = sorted(lclstfreq, key=itemgetter(1), reverse=True)
    remap = [i for i, _ in lclstfreq]

    for exp, nfile in nfiles:
        log = generate_log(exp, clpeaks, timepeaks, remap, gap=200)

        nev = 0
        cons = 0
        sec = 1412114700
        cases = []
        for ev in log:
            case = {'key': 'Event %d' % nev}
            nev += 1
            ltrans = []
            for e in ev:
                trans = {'who': 'cat', 'when': time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime(sec+(cons*60))), 'to': e}
                ltrans.append(trans)
                cons +=1
            case['transitions'] = ltrans
            cases.append(case)

        write_xes('PM-'+line+'-'+nfile, rpath, cases)




cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/'
rpath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/'
ipath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/icons/'
ocpath = '/home/bejar/Documentos/Investigacion/cinvestav/'

nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
          (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
          ]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# aline = [('L4cd', 'k9.n5', 9),
#          ('L4ci', 'k9.n1', 9),
#         ('L5cd', 'k10.n6' , 10),
#         #('L5rd', 'k20.n1' ),
#         ('L5ci', 'k15.n1', 15),
#         ('L5ri', 'k15.n9', 15),
#         ('L6cd', 'k17.n1', 17),
#         ('L6rd', 'k13.n9', 13),
#         #('L6ci', 'k15.n1'),
#         ('L6ri', 'k18.n4', 18),
#         ('L7ri', 'k18.n4', 18)
#         ]
aline = [
         ('L6ri', 'k18.n4', 18)
        ]


# line = 'L6ri'  # 'L6rd' 'L5ci' 'L6ri'
# clust = '.k15.n1'  # '.k20.n5' '.k16.n4' '.k15.n1'

for line, clust, _ in aline:
    matpeaks = scipy.io.loadmat(cpath + '/Selected/centers.' + line + '.' + clust + '.mat')
    mattime = scipy.io.loadmat(cpath + '/WholeTime.' + line + '.mat')

    clpeaks = matpeaks['IDX']
    timepeaks = mattime['temps'][0]


    generate_model_log(line)