"""
.. module:: ComputeTimeline

ComputeTimeline
*************

:Description: ComputeTimeline

    

:Authors: bejar
    

:Version: 

:Created on: 07/11/2014 7:55 

"""

__author__ = 'bejar'


import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from util.distances import sKLD, square_frobenius, renyihalf
from util.misc import  peaks_sequence, find_time_end, probability_matrix_seq, probability_matrix_multi
from util.plots import plotSignals
from util.paths import cpath, rpath

# def timeline(clpeaks, timepeaks, nfiles, line, gap, step):
#     for exp, nfile in nfiles:
#         compute_timeline(exp, clpeaks, timepeaks, line+'-'+nfile, gap=gap, step=step)
#
#
# def compute_timeline(nexp, clpeaks, timepeaks, nfile, gap=0, step=1000):
#     """
#     Computes the time line of the probability matrix of transitions
#
#     :param nexp:
#     :param clpeaks:
#     :param timepeaks:
#     :param sup:
#     :param nfile:
#     :param remap:
#     :param gap:
#     :param step:
#     :return:
#     """
#     # Select the index of the experiment
#     peakini = 0
#     i = 0
#     while i < nexp:
#         exp = timepeaks[i]
#         peakini += exp.shape[0]
#         i += 1
#
#     exp = timepeaks[nexp]
#     #print exp.shape[0]
#     peakend = peakini + exp.shape[0]
#
#     # Build the sequence string
#     peakstr, peaksfreq = peaks_sequence(clpeaks, nexp, peakini, peakend, gap)
#     nsym = len(peaksfreq)
#
#
#     # First probability matrix
#     current = 0
#     last = find_time(exp, current, step)
#     pmcurr = probability_matrix(peakstr, current, last, nsym)
#     current = last + 1
#     last = find_time(exp, current, step)
#     while current < exp.shape[0]-1:
# #        print current, last
#         pmnext = probability_matrix(peakstr, current, last, nsym)
#         diff = dfuns[dist](pmcurr, pmnext)
#         print diff
#         current = last + 1
#         last = find_time(exp, current, step)
#
# # def compute_timeline_overlapped(nexp, clpeaks, timepeaks, gap=0, step=100, length=1000, laplace=0.0, dist='Frobenius'):
#     """
#     Computes the time line of the probability matrix of transitions
#
#     :param nexp:
#     :param clpeaks:
#     :param timepeaks:
#     :param sup:
#     :param nfile:
#     :param remap:
#     :param gap:
#     :param step:
#     :return:
#     """
#     # Select the index of the experiment
#     peakini = 0
#     i = 0
#     while i < nexp:
#         exp = timepeaks[i]
#         peakini += exp.shape[0]
#         i += 1
#
#     exp = timepeaks[nexp]
#     #print exp.shape[0]
#     peakend = peakini + exp.shape[0]
#
#     # Build the sequence
#     peakstr, peaksfreq = peaks_sequence(clpeaks, timepeaks, nexp, peakini, peakend, gap)
#     nsym = len(peaksfreq)
#     print peakstr
#
#     # First probability matrix
#     current = 0
#     last = find_time(exp, current, length)
#     pmcurr = probability_matrix(peakstr, current, last, nsym, laplace=laplace)
#     current = find_time(exp, current, step)
#     last = find_time(exp, current, length)
#     ldist = []
#     while last < exp.shape[0]-1:
# #        print current, last
#         pmnext = probability_matrix(peakstr, current, last, nsym, laplace=laplace)
#         ldist.append(dfuns[dist](pmcurr, pmnext))
#         #print diff
#         current = find_time(exp, current, step)
#         last = find_time(exp, current, length)
#         pmcurr = pmnext
#
#     return ldist
#


def timeline_overlapped(clpeaks, timepeaks, nfiles, line, ncl, gap=300, step=50*300, length=300*300, laplace=0.0, dist='Frobenius', multi=True):
    ldiffs = []
    for exp, nfile in nfiles:
        ldiffs.append((compute_timeline_overlapped(exp,
                       clpeaks, ncl, timepeaks, gap=gap, step=step,
                       length=length, laplace=laplace, dist=dist, multi=multi), nfile+'-'+dist))
    vmax = [max(x) for x,_ in ldiffs]
    vmin = [min(x) for x,_ in ldiffs]

    name = line + '-timelineG%d-S%d-L%d-Lap%2.2f-%s' % (round(gap*.6,0), round(step * .0006,0), round(length * .0006,0),laplace,dist)
    title = line + '-timeline G= %2.3f S=%2.1f L=%2.1f Lap=%2.2f D=%s' % (gap*.0006, step * .0006, length * .0006, laplace, dist)

    if multi:
        name += '-Multi'
        title += ' Multi=True'

    # print line,
    #
    # for l, _ in ldiffs:
    #     print '& ','%2.2e' % np.mean(l),
    #
    # print '\\\\\\hline'

    plotSignals(ldiffs, 6, 2, max(vmax), min(vmin), name, title)


def compute_timeline_overlapped(nexp, clpeaks, ncl, timepeaks, gap=0, step=100, length=1000, laplace=0.0, dist='Frobenius', multi=True):
    """
    Computes the time line of the probability matrix of transitions

    :param nexp:
    :param clpeaks:
    :param timepeaks:
    :param sup:
    :param nfile:
    :param remap:
    :param gap:
    :param step:
    :return:
    """
    # Select the index from clpeaks where the experiment begins
    # adding all the sizes of the timepeaks arrays until the experiment number
    peakini = 0
    i = 0
    while i < nexp:
        peakini += timepeaks[i].shape[0]
        i += 1

    exp = timepeaks[nexp]
    #print exp.shape[0]
    peakend = peakini + exp.shape[0]

    # Build the sequence
    peakseq, _ = peaks_sequence(clpeaks, timepeaks, nexp, peakini, peakend, gap)
    nsym = ncl
    # First probability matrix
    current = 0
    last = find_time_end(peakseq, current, length)
    if multi:
        pmcurr = probability_matrix_multi(peakseq, current, last, nsym, gap=gap, laplace=laplace)
    else:
        pmcurr = probability_matrix_seq(peakseq, current, last, nsym, gap=gap, laplace=laplace)

    current = find_time_end(peakseq, current, step)
    last = find_time_end(peakseq, current, length)


    ldist = []
    while last < len(peakseq)-1:
        if multi:
            pmnext = probability_matrix_multi(peakseq, current, last, nsym, gap=gap, laplace=laplace)
        else:
            pmnext = probability_matrix_seq(peakseq, current, last, nsym, gap=gap, laplace=laplace)

        ldist.append(dfuns[dist](pmcurr, pmnext))
        #print diff
        current = find_time_end(peakseq, current, step)
        last = find_time_end(peakseq, current, length)
        pmcurr = pmnext

    return ldist

def do_the_job(gap, step, length, laplace, dist, multi):
    for line, clust, ncl in aline:

        print line, clust
        matpeaks = scipy.io.loadmat( cpath + '/centers.' + line + '.' + clust + '.mat')
        mattime = scipy.io.loadmat( cpath + '/WholeTime.' + line + '.mat')

        clpeaks = matpeaks['IDX']
        timepeaks = mattime['temps'][0]
        timeline_overlapped(clpeaks, timepeaks, nfiles, line, ncl, gap=gap, step=step, length=length, laplace=laplace, dist=dist, multi=multi)


nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
          (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
          ]

# nfiles = [(0, 'ctrl1')]


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


# aline = [('L4ci', 'k20.n1')]

# line = 'L5ci'  # 'L6rd' 'L5ci' 'L6ri'
# clust = '.k16.n4'  # '.k20.n5' '.k16.n4' '.k15.n1'

# 300 = 180ms

dfuns ={'Renyi': renyihalf, 'Frobenius': square_frobenius, 'KL': sKLD}

gap = int(400.0 / 0.6) #ms
step = int(3.0 / 0.0006) #s
length = int(60.0 / 0.0006) #s
dist = 'Renyi'
laplace = 1
multi = True

#for i in [60.0,90.0, 120.0,180.0,240.0,300.0]:
for i in [60.0, 90.0, 120.0, 180.0, 240.0, 300.0]:
   # print '\\begin{tabular}','{|c|',
   # print 'c|'*len(nfiles), '}\\\\\\hline'
   # print '%2.2fs'%i,
   # for _, l in nfiles:
   #     print '& ', l,
   # print '\\\\\hline'
    length = int(i / 0.0006) #s
    do_the_job(gap, step, length, laplace, dist, multi)
   # print '\\end{tabular}'
   # print
