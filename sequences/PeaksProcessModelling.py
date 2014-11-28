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
    peakstr = {}
    peakset = []

    for i in range(peakini, peakend):
        peakset.append(voc[remap[clpeaks[i][0]-1]])
        if i < peakend-1 and gap != 0:
            if (timepeaks[nexp][i-peakini+1] - timepeaks[nexp][i-peakini]) > gap:
                if peakset not in peakstr:
                    peakstr.append(peakset)
                    peakset = []

    return peakstr

def generate_model_log():
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
        print log
        # lm = Alpha(log)
        # pn = PetriNet()
        # pn.from_alpha(lm, dotfile="{}.dot".format(rpath+line+'-'+nfile))




cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/'
rpath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/'
ipath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/icons/'
ocpath = '/home/bejar/Documentos/Investigacion/cinvestav/'

# nfiles = [(0, 1, 'ctrl1'), (1, 1, 'ctrl2'), (2, 1, 'capsa1'), (3, 1, 'capsa2'), (4, 1, 'capsa3'),
#           (5, 1, 'lido1'), (6, 1, 'lido2'), (7, 1, 'lido3'), (8, 1, 'lido4'), (9, 1, 'lido5'), (10, 1, 'lido6')
#           ]
nfiles = [(2, 'capsa1')
          ]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
line = 'L6ri'  # 'L6rd' 'L5ci' 'L6ri'
clust = '.k15.n1'  # '.k20.n5' '.k16.n4' '.k15.n1'

matpeaks = scipy.io.loadmat( cpath + '/centers.' + line + clust + '.mat')
mattime = scipy.io.loadmat( cpath + '/WholeTime.' + line + '.mat')

clpeaks = matpeaks['IDX']
timepeaks = mattime['temps'][0]


generate_model_log()