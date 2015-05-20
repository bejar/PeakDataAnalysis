"""
.. module:: TimelineSpace

TimelineSpace
*************

:Description: TimelineSpace

    

:Authors: bejar
    

:Version: 

:Created on: 14/11/2014 11:04 

"""

__author__ = 'bejar'

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import MDS, TSNE, SpectralEmbedding
from mpl_toolkits.mplot3d import Axes3D

from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence
from util.misc import peaks_sequence, find_time_end, probability_matrix_multi
from config.paths import datapath


def compute_timeline_pmatrices(nexp, clpeaks, ncl, timepeaks, gap=0, step=100, length=1000, laplace=0.0,
                               dist='Frobenius'):
    """
    Returns the probability matrices of a timeline

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
    # print exp.shape[0]
    peakend = peakini + exp.shape[0]

    # Build the sequence
    peakseq, peaksfreq = peaks_sequence(clpeaks, timepeaks, nexp, peakini, peakend, gap)
    nsym = ncl

    # First probability matrix
    current = 0
    last = find_time_end(peakseq, current, length)
    pmcurr = probability_matrix_multi(peakseq, current, last, nsym, gap=gap, laplace=laplace)
    ldist = []
    while last < len(peakseq) - 1:
        ldist.append(pmcurr)
        current = find_time_end(peakseq, current, step)
        last = find_time_end(peakseq, current, length)
        pmcurr = probability_matrix_multi(peakseq, current, last, nsym, gap=gap, laplace=laplace)

    return ldist


def compute_trans_dist(lmtrans):
    """
    computes a distance matrix with all the transition matrices
    :param lmtrans:
    :return:
    """

    dmatrix = np.zeros((len(lmtrans), len(lmtrans)))
    for i in range(len(lmtrans)):
        for j in range(len(lmtrans)):
            dmatrix[i, j] = dfuns[dist](lmtrans[i], lmtrans[j])
    return dmatrix


# def timeline_overlapped(nfiles, gap=300, step=50*300, length=300*300, laplace=0.0):
# for exp, nfile in nfiles:
#         lmtrans = compute_timeline_pmatrices(exp, clpeaks, timepeaks, line+'-'+nfile, gap=gap, step=step, length=length, laplace=laplace)
#         mdist = compute_trans_dist(lmtrans)
#         fig = plt.figure()
#         mds = MDS(n_components=3, dissimilarity='precomputed')
#         #mds = TSNE(n_components=3, perplexity=50.0, early_exaggeration=20.0, learning_rate=500.0, metric='precomputed')
#         X_new = mds.fit_transform(mdist)
#         ax = fig.gca(projection='3d')
#         y = range(0,len(lmtrans))
#         pl.scatter(X_new[:, 1], X_new[:, 2], zs=X_new[:, 0], c=y,  s=25)
#         plt.show()
#

def timeline_overlapped_exp(clpeaks, ncl, timepeaks, nfiles, gap=300, step=50 * 300, length=300 * 300, laplace=0.0):
    ldiffs = []
    for exp, _, nfile in nfiles:
        lmtrans = compute_timeline_pmatrices(exp, clpeaks, ncl, timepeaks, gap=gap, step=step, length=length,
                                             laplace=laplace)
        print len(lmtrans)
        ldiffs.append(lmtrans)

    # for i in range(len(ldiffs)-1):
    #     for j in range(i+1, len(ldiffs)):
    md = []
    y = []
    for l in ldiffs:
        md.extend(l)
    i = 0
    for l in ldiffs:
        y.extend([nfiles[i][1]] * len(l))
        i += 1
    #print len(ldiffs[i]), len(ldiffs[j]), len(y), len(md)
    mdist = compute_trans_dist(md)
    fig = plt.figure()
    #mds = MDS(n_components=3, dissimilarity='precomputed')
    #mds = TSNE(n_components=3, perplexity=50.0, early_exaggeration=2.0, learning_rate=50.0, n_iter=2000, metric='precomputed')
    mds = SpectralEmbedding(n_components=3, affinity='precomputed', n_neighbors=5)
    X_new = mds.fit_transform(mdist)
    #print 'STRESS = ', mds.stress_
    ax = fig.gca(projection='3d')
    plt.scatter(X_new[:, 1], X_new[:, 2], zs=X_new[:, 0], c=y, s=25)
    #plt.scatter(X_new[:, 0], X_new[:, 1], c=y)
    plt.show()


nfiles = [(0, '#0000FF', 'ctrl1'), (5, '#FF0000', 'lido1'), (2, '#00FF00', 'capsa1')
          ]


# nfiles = [(0, '#0000FF', 'ctrl1'), (1, '#000077', 'ctrl2'),
#           (5, '#FF0000', 'lido1'), (6, '#FFFFFF', 'lido2'), (7, '#AA0000', 'lido3'), (10, '#770000', 'lido6'),
#           (2, '#00FF00', 'capsa1'), (3, '#00AA00', 'capsa2'), (4, '#007700', 'capsa3')]

# nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
#           (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
#           ]

#nfiles = [(0, 'ctrl1')]

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

dfuns = {'Renyi': renyi_half_divergence, 'Frobenius': square_frobenius_distance, 'KL': simetrized_kullback_leibler_divergence}

gap = int(300.0 / .6)  #ms
step = int(6.0 / 0.0006)  #s
length = int(120.0 / 0.0006)  #s
dist = 'Frobenius'

for line, clust, ncl in aline:
    name = line + '-timelineG%d-S%d-L%d' % (round(gap * .6, 0), round(step * .0006, 0), round(length * .0006, 0))
    print name, gap, step, length
    title = line + '-timeline G= %2.3f S=%2.1f L=%2.1f' % (gap * .0006, step * .0006, length * .0006)
    matpeaks = scipy.io.loadmat(datapath + 'Selected/centers.' + line + '.' + clust + '.mat')
    mattime = scipy.io.loadmat(datapath + '/WholeTime.' + line + '.mat')

    clpeaks = matpeaks['IDX']
    timepeaks = mattime['temps'][0]
    timeline_overlapped_exp(clpeaks, ncl, timepeaks, nfiles, gap=gap, step=step, length=length, laplace=1)