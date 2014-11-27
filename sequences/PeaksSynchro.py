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
import pylab as P
from pylab import *
from util.plots import plotMatrices
from util.misc import normalize_matrix

def gen_data_matrix(lines):
    """
    Generates a datastructure to store the peaks coincidences
    :param lines:
    :return:
    """

    mtrx = []
    for i in range(len(lines)):
        imtrx = []
        for j in range(len(lines)):
            if i != j:
                imtrx.append(np.zeros((lines[i][2], lines[j][2])))
            else:
                imtrx.append(None)
        mtrx.append(imtrx)
    return mtrx


def compute_sequences(clpeaks, timepeaks, lines, nexp, remap):
    """
    Computes the synchronization of the peaks of several lines for an experiment

    :param lines:
    :param exps:
    :param window:
    :return:
    """
    peakseq = []
    for line, _, _ in lines:
        peakini = 0
        i = 0
        while i < nexp:
            exp = timepeaks[line][i]
            peakini += exp.shape[0]
            i += 1

        exp = timepeaks[line][nexp]
        peakend = peakini + exp.shape[0]

        # Build the sequence of peaks
        peakstr = []
        for i in range(peakini, peakend):
            peakstr.append([remap[line][clpeaks[line][i][0]-1]-1, exp[i-peakini][0]])
        peakseq.append(peakstr)
    return peakseq


def compute_synchs(seq, window=15):
    def minind():
        """
        computes the index of the sequence with the lower value
        """
        mind = 0
        mval = float('inf')
        for i in range(len(seq)):
            if (len(seq[i]) > counts[i]) and (seq[i][counts[i]][1] < mval):
                mind = i
                mval = seq[i][counts[i]][1]
        return mind

    # Contadores de avance
    counts = [0]*len(seq)

    fin = False
    lsynch = []
    while not fin:
        # Compute the peak with the lower value
        imin = minind()
        # Look for the peaks inside the window length
        psynch = [(imin, seq[imin][counts[imin]])]
        for i in range(len(seq)):
            if (len(seq[i]) > counts[i]) and (i!=imin):
                if seq[i][counts[i]][1] <= (seq[imin][counts[imin]][1]+window):
                    psynch.append((i, seq[i][counts[i]]))
                    counts[i] += 1
        counts[imin] += 1
        if len(psynch) > 1:
            lsynch.append(psynch)
            #print psynch


        # We finish when all the counters have passed the lengths of the sequences
        fin = True
        for i in range(len(seq)):
            fin = fin and (counts[i] == len(seq[i]))
    return lsynch


def generate_synchs(lines, exps, window=15):
    """
    Generates a list of synchonized peaks

    :param lines:
    :param exps:
    :param window:
    :return:
    """

    clpeaks = {}
    timepeaks = {}
    remap = {}
    for line, clust, _ in aline:
        matpeaks = scipy.io.loadmat(cpath + '/Selected/centers.' + line + '.' + clust + '.mat')
        mattime = scipy.io.loadmat(cpath + '/WholeTime.' + line + '.mat')

        clpeaks[line] = matpeaks['IDX']
        timepeaks[line] = mattime['temps'][0]
        remap[line] = compute_remap(clpeaks[line], timepeaks[line])
    lsynch = []
    for nexp, exp in exps:
        sequ = compute_sequences(clpeaks, timepeaks, lines, nexp, remap)
        syn = compute_synchs(sequ, window=window)
        lsynch.append([exp, syn])

    return lsynch


def length_synch_frequency_histograms(lsynch):
    """
    Histograms of the frequencies of the lengths of the synchronizations
    :param lsynch:
    :return:
    """
    for line, peaks in lsynch:
        print line
        x = []
        for pk in peaks:
            x.append(len(pk))

        P.figure()
        n, bins, patches = P.hist(x, max(x)-1, normed=1, histtype='bar', fill=True)
        P.show()


def compute_remap(clpeaks, timepeaks):
    """
     Computes the remaps of the peaks indices using the frequency of the peaks
     of the first experiment

    :param clpeaks:
    :param timepeaks:
    :return:
    """
    clstfreq = {}

    for i in range(0, timepeaks[0].shape[0]):
        if clpeaks[i][0] in clstfreq:
            clstfreq[clpeaks[i][0]] += 1
        else:
            clstfreq[clpeaks[i][0]] = 1

    lclstfreq = [(k, clstfreq[k]) for k in clstfreq]
    lclstfreq = sorted(lclstfreq, key=itemgetter(1), reverse=True)
    remap = [i for i, _ in lclstfreq]

    return remap


def gen_peaks_contingency(peakdata):
    """
    Generates PDFs with the association frequencies of the peaks

    :return:
    """
    for nx in range(len(nfiles)):
        print nfiles[nx][1]
        pk = peakdata[nx]

        dmatrix = gen_data_matrix(aline)

        for p in pk[1]:
            #print p
            for ei in p:
                for ej in p:
                    if ei[0] != ej[0]:
                        #print ei[0], ej[0], ei[1][0], ej[1][0]
                        m = dmatrix[ei[0]][ej[0]]
                        m[ei[1][0]][ej[1][0]] += 1
                        m = dmatrix[ej[0]][ei[0]]
                        m[ej[1][0]][ei[1][0]] += 1


        for ln in range(len(aline)):
            mt = dmatrix[ln]
            lplot = []
            for i in range(len(aline)):
                if i != ln:
                    lplot.append((normalize_matrix(mt[i]), aline[i][0]))

            plotMatrices(lplot, 4, 2, 'msynch-'+nfiles[nx][1]+'-'+aline[ln][0], aline[ln][0])



nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
         (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
         ]

# nfiles = [ (8, 'lido4'), (9, 'lido5')]

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# aline = [#('L4cd', 'k19.n1'),
#          ('L4ci', 'k20.n1', 20),
#         ('L5cd', 'k10.n1', 10),
#         #('L5rd', 'k20.n1' ),
#         ('L5ci', 'k21.n1', 21),
#         ('L5ri', 'k20.n1', 20),
#         ('L6cd', 'k17.n1', 17),
#         ('L6rd', 'k20.n1', 20),
#         ('L6ci', 'k15.n1', 15),
#         ('L6ri', 'k18.n1', 18),
#         ('L7ri', 'k18.n1', 18)
#         ]

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

peakdata = generate_synchs(aline, nfiles, window=15)

# print len(peakdata)
#
# for l in peakdata:
#     print l[0], len(l[1])
#     print l[1]

### Histograms of the frequency of the lengths
length_synch_frequency_histograms(peakdata)

### Contingency PDFs
#gen_peaks_contingency(peakdata)