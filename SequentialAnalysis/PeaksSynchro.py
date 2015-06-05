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
import pylab as P
from pylab import *
from pyx import *

from config.paths import datapath, seqpath
from util.plots import plotMatrices, plotMatrix
from util.misc import normalize_matrix, compute_frequency_remap
import h5py
from sklearn.decomposition import PCA
import numpy as np

from config.experiments import experiments
from util.plots import show_signal
from joblib import Parallel, delayed
from sklearn.metrics import pairwise_distances_argmin_min








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
    Computes the sequence of peaks of different lines

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
            peakstr.append([remap[line][clpeaks[line][i][0] - 1] - 1, exp[i - peakini][0]])
        peakseq.append(peakstr)
    return peakseq





def gen_peaks_contingency(dfile, peakdata, sensors):
    """
    Generates PDFs with the association frequencies of the peaks

    :return:
    """
    for _, nx in dfile:
        print nx
        pk = peakdata[nx]

        dmatrix = gen_data_matrix(sensors)

        for p in pk:
            # print p
            for ei in p:
                for ej in p:
                    if ei[0] != ej[0]:
                        #print ei[0], ej[0], ei[1][0], ej[1][0]
                        m = dmatrix[ei[0]][ej[0]]
                        m[ei[1][0]][ej[1][0]] += 1
                        # m = dmatrix[ej[0]][ei[0]]
                        # m[ej[1][0]][ei[1][0]] += 1
                        #

        for ln in range(len(sensors)):
            mt = dmatrix[ln]
            lplot = []
            for i in range(len(sensors)):
                if i != ln:
                    lplot.append((normalize_matrix(mt[i]), sensors[i]))

            plotMatrices(lplot, 4, 2, 'msynch-' + nx + '-' + sensors[ln][0], sensors[ln])


def lines_coincidence_matrix(peakdata, sensors):
    """
    Computes a contingency matrix of how many times two lines have been synchronized

    :param peakdata:
    :return:
    """
    coinc = np.zeros((len(sensors), len(sensors)))

    for syn in peakdata:
        for i in syn:
            for j in syn:
                if i[0] != j[0]:
                    coinc[i[0], j[0]] += 1

    return coinc


def correlation_exp(peakdata, exps, sensors, expcounts, window):
    """
    Computes the mutual information of the lines
    :param peakdata:
    :param expcounts:
    :return:
    """
    for exp in exps:
        # print exp
        cmatrix = lines_coincidence_matrix(peakdata[exp])
        corrmatrix = np.zeros((len(sensors), len(sensors)))
        for i in range(len(sensors)):
            for j in range(len(sensors)):
                if i != j:
                    cab = cmatrix[i, j]
                    ca = expcounts[exp][i]
                    cb = expcounts[exp][j]
                    tot = (ca + cb - cab) * 1.0
                    corrmatrix[i, j] = cab / tot
        corrmatrix[0, 0] = 1.0
        plotMatrix(corrmatrix, exp + '-W' + str(int(window * 0.1)) + 'ms', exp + '-W' + str(int(window * 0.1)) + 'ms',
                   [x for x in range(len(sensors))], [x for x in sensors])
        #print '----'

# --------------------------------------------------------------------------------------------------------------------

voc = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

coormap = {'L4ci': (1, 1),
           'L4cd': (1, 2),
           'L5ri': (2, 1),
           'L5rd': (2, 2),
           'L5ci': (3, 1),
           'L5cd': (3, 2),
           'L6rd': (4, 1),
           'L6ri': (4, 2),
           'L6ci': (5, 1),
           'L6cd': (5, 2),
           'L7ri': (6, 1),
           'L7rd': (6, 2)
           }

###
#peakdata, expcounts = generate_synchs(aline, nfiles, window=int(round(window)))
####
#correlation_exp(peakdata, expcounts, int(round(window)))

###
#draw_synchs(peakdata, nfiles, window=int(round(window*0.6)))

# print expcounts
#
# for p in peakdata:
#     print p
# print len(peakdata)
#
# for l in peakdata:
#     print l[0], len(l[1])
#     for p in l[1]:
#         print p

### Histograms of the frequency of the lengths
#length_synch_frequency_histograms(peakdata, window=int(round(window * 0.6)))

### Contingency PDFs
#gen_peaks_contingency(peakdata)



def length_synch_frequency_histograms( dsynchs, exps, window):
    """
    Histograms of the frequencies of the lengths of the synchronizations
    :param lsynch:
    :return:
    """
    for line in exps:
        print line
        x = []
        for pk in dsynchs[line]:
            x.append(len(pk))

        P.figure()
        n, bins, patches = P.hist(x, max(x) - 1, normed=1, histtype='bar', fill=True)
        P.title('%s-W%d' % (line, window), fontsize=48)
        P.savefig(seqpath + '/histo-' + line + '-W' + str(window) + '.pdf', orientation='landscape', format='pdf')



def draw_synchs(peakdata, exps, sensors, window):
    """
    Generates a PDF of the synchronizations

    :param peakdata:
    :param exps:
    :param window:
    :return:
    """
    def syncIcon(x, y, sensors, coord, lv, scale, can):
        scale *= 0.6
        y = (y / 2.5) + 2
        x += 5

        for al, v in zip(sensors, lv):
            c = coord[al]
            p = path.rect(y + (c[0] * scale), x + (c[1] * scale), scale, scale)
            if v:
                can.stroke(p, [deco.filled([color.gray(0.5)])])
            else:
                can.stroke(p)

    for exp in exps:
        print exp
        ncol = 0
        npage = 1
        lpages = []
        pk = peakdata[exp]
        c = canvas.canvas()
        p = path.line(1, 0, 1, 28)
        c.stroke(p)
        c.text(1.5, 27, '%s - page: %d' % (exp, npage), [text.size(-1)])
        vprev = 0
        y = 0
        yt = 1.25
        for i in range(len(pk)):
            l = [False] * len(sensors)
            for p in pk[i]:
                l[p[0]] = True

            v = np.min([t for _, t in pk[i]]) % 5000
            if v < vprev:
                p = path.line(yt + 2.5, 0, yt + 2.5, 28)
                c.stroke(p)
                y += 6.3
                yt += 2.5
                ncol += 1
                if ncol % 7 == 0:
                    # p=path.line(yt+2.5, 0, yt+2.5, 28)
                    # c.stroke(p)
                    npage += 1
                    ncol = 0
                    lpages.append(document.page(c))
                    c = canvas.canvas()
                    p = path.line(1, 0, 1, 28)
                    c.stroke(p)
                    c.text(1.5, 27, '%s - page: %d' % (exp, npage), [text.size(-1)])
                    vprev = 0
                    y = 0
                    yt = 1.25

            vprev = v
            d = v - 800
            c.text(yt, (d / 200.0) + 5.25, '%8s' % str(int(round(pk[i][0][1] * 0.6))), [text.size(-4)])
            syncIcon(d / 200.0, y, sensors, coormap, l, 0.25, c)

        # p=path.line(yt+2.5, 0, yt+2.5, 28)
        # c.stroke(p)

        d = document.document(lpages)

        d.writePDFfile(datainfo.dpath + "/Results/peaksynchs-%s-W%d" % (datainfo.name, window))

def compute_synchs(seq, window=15):
    """
    Computes the synchronizations of the peaks of several lines
    :param seq:
    :param window:
    :return:
    """

    def minind():
        """
        computes the index of the sequence with the lower value
        """
        mind = 0
        mval = float('inf')
        for i in range(len(seq)):
            if (len(seq[i]) > counts[i]) and (seq[i][counts[i]] < mval):
                mind = i
                mval = seq[i][counts[i]]
        return mind

    # Contadores de avance
    counts = [0] * len(seq)

    fin = False
    lsynch = []
    while not fin:
        # Compute the peak with the lower value
        imin = minind()
        if len(seq[imin]) > counts[imin] + 1 and \
            seq[imin][counts[imin]] <= (seq[imin][counts[imin] + 1] + window):
            # Look for the peaks inside the window length
            psynch = [(imin, seq[imin][counts[imin]])]
            for i in range(len(seq)):
                if (len(seq[i]) > counts[i]) and (i != imin):
                    if seq[i][counts[i]] <= (seq[imin][counts[imin]] + window):
                        psynch.append((i, seq[i][counts[i]]))
                        counts[i] += 1
            counts[imin] += 1
            if len(psynch) > 1:
                lsynch.append(psynch)
                # print psynch
        else:
            counts[imin] += 1

        # We finish when all the counters have passed the lengths of the sequences
        fin = True
        for i in range(len(seq)):
            fin = fin and (counts[i] == len(seq[i]))
    return lsynch



def compute_data_labels(dfile, sensor):
    """
    Computes the labels of the data using the centroids of the cluster in the file
    :param dfile:
    :param sensor:
    :return:
    """
    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

    d = f[dfile + '/' + sensor + '/Clustering/' + 'Centers']
    centers = d[()]
    d = f[dfile + '/' + sensor + '/' + 'PeaksResamplePCA']
    data = d[()]
    labels, _ = pairwise_distances_argmin_min(data,centers)
    return labels


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    window = 250
    print 'W=', int(round(window))
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    #lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e140515b']

    TVD = False
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]

        dfile = datainfo.datafiles[0]
        #for dfile in datainfo.datafiles:
        print dfile
        lsens_labels = []

        # compute the labels of the data
        # for sensor in datainfo.sensors:
        #     print sensor
        #     lsens_labels.append((sensor, compute_data_labels(dfile, sensor)))

        # Times of the peaks
        ltimes = []
        for sensor in datainfo.sensors:
            f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')
            d = f[dfile + '/' + sensor + '/' + 'Time']
            data = d[()]
            ltimes.append(data)

        lsynchs = compute_synchs(ltimes, window=window)

        # print len(lsynchs)
        # for i in  lsynchs:
        #     print i, len(i)

        peakdata[dfile] = lsynchs
        #draw_synchs(peakdata, [dfile], datainfo.sensors, window)
        length_synch_frequency_histograms(peakdata, [dfile], window=int(round(window * 0.6)))