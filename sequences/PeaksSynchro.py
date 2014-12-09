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
from util.plots import plotMatrices, plotMatrix
from util.misc import normalize_matrix, compute_frequency_remap
from pyx import *

def mintime(ltimes):
    mt = np.inf

    for _, t in ltimes:
        if mt > t[1]:
            mt = t[1]
    return mt


def syncIcon(x, y, lines, coord, lv, scale, can):
    scale=scale*0.6
    y=(y/2.5)+2
    x=x+5


    #lcoor=[(i,j) for i in range(n) for j in range(m)]

    for al,v in zip(aline, lv):
        c = coord[al[0]]
        p=path.rect(y+(c[0]*scale), x+(c[1]*scale), scale, scale)
        if v:
            can.stroke(p, [deco.filled([color.gray(0.5)])])
        else:
            can.stroke(p)


def draw_synchs(peakdata, exps, window):

    for _, exp in exps:
        print exp
        ncol = 0
        npage = 1
        lpages = []
        pk = peakdata[exp]
        c = canvas.canvas()
        p = path.line(1, 0, 1, 28)
        c.stroke(p)
        c.text(1.5, 27, '%s - page: %d'% (exp, npage), [text.size(-1)])
        vprev = 0
        y = 0
        yt = 1.25
        for i in range(len(pk)):
            l = [False] * len(aline)
            for p in pk[i]:
                l[p[0]] = True

            v = mintime(pk[i]) % 5000
            if v < vprev:
                p=path.line(yt+2.5, 0, yt+2.5, 28)
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
            c.text(yt, (d/200.0)+5.25, '%8s' % str(int(round(pk[i][0][1][1]*0.6))), [text.size(-4)])
            syncIcon(d/200.0, y, aline, coormap, l, 0.25, c)

        # p=path.line(yt+2.5, 0, yt+2.5, 28)
        # c.stroke(p)

        d = document.document(lpages)

        d.writePDFfile(rpath+"/peaksynchs-%s-W%d" % (exp, window))

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
    Computes the seguqnce of peaks of different lines

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
        if len(seq[imin]) > counts[imin]+1 and seq[imin][counts[imin]][1] <= (seq[imin][counts[imin]+1][1]+window):
            # Look for the peaks inside the window length
            psynch = [(imin, seq[imin][counts[imin]])]
            for i in range(len(seq)):
                if (len(seq[i]) > counts[i]) and (i != imin):
                    if seq[i][counts[i]][1] <= (seq[imin][counts[imin]][1]+window):
                        psynch.append((i, seq[i][counts[i]]))
                        counts[i] += 1
            counts[imin] += 1
            if len(psynch) > 1:
                lsynch.append(psynch)
                #print psynch
        else:
            counts[imin] += 1

        # We finish when all the counters have passed the lengths of the sequences
        fin = True
        for i in range(len(seq)):
            fin = fin and (counts[i] == len(seq[i]))
    return lsynch


def generate_synchs(lines, exps, window=15):
    """
    Returns a diccionary for all the experiments of synchonized peaks and
    another diccionary for all experiments of the counts of the peaks

    :param lines:
    :param exps:
    :param window:
    :return:
    """

    clpeaks = {}
    timepeaks = {}
    remap = {}

    ## Computes the peaks remapping for all the lines
    for line, clust, _ in aline:
        matpeaks = scipy.io.loadmat(cpath + '/Selected/centers.' + line + '.' + clust + '.mat')
        mattime = scipy.io.loadmat(cpath + '/WholeTime.' + line + '.mat')

        clpeaks[line] = matpeaks['IDX']
        timepeaks[line] = mattime['temps'][0]
        remap[line] = compute_frequency_remap(timepeaks[line], clpeaks[line])

    ## Synchronizations for the different experiments
    dsynch = {}
    peakcounts = {}

    for nexp, exp in exps:
        sequ = compute_sequences(clpeaks, timepeaks, lines, nexp, remap)
        expcounts = {}
        for i in range(len(sequ)):
            expcounts[aline[i][0]] = len(sequ[i])
        peakcounts[exp] = expcounts
        syn = compute_synchs(sequ, window=window)
        dsynch[exp] = syn

    return dsynch, peakcounts


def length_synch_frequency_histograms(dsynchs, window):
    """
    Histograms of the frequencies of the lengths of the synchronizations
    :param lsynch:
    :return:
    """
    for _, line in nfiles:
        print line
        x = []
        for pk in dsynchs[line]:
            x.append(len(pk))

        P.figure()
        n, bins, patches = P.hist(x, max(x)-1, normed=1, histtype='bar', fill=True)
        P.title('%s-W%d'%(line, window), fontsize=48)
        P.savefig(rpath+'/histo-'+line+'-W'+str(window)+'.pdf', orientation='landscape', format='pdf')



def gen_peaks_contingency(peakdata):
    """
    Generates PDFs with the association frequencies of the peaks

    :return:
    """
    for _, nx in nfiles:
        print nx
        pk = peakdata[nx]

        dmatrix = gen_data_matrix(aline)

        for p in pk:
            #print p
            for ei in p:
                for ej in p:
                    if ei[0] != ej[0]:
                        #print ei[0], ej[0], ei[1][0], ej[1][0]
                        m = dmatrix[ei[0]][ej[0]]
                        m[ei[1][0]][ej[1][0]] += 1
                        # m = dmatrix[ej[0]][ei[0]]
                        # m[ej[1][0]][ei[1][0]] += 1
                        #

        for ln in range(len(aline)):
            mt = dmatrix[ln]
            lplot = []
            for i in range(len(aline)):
                if i != ln:
                    lplot.append((normalize_matrix(mt[i]), aline[i][0]))

            plotMatrices(lplot, 4, 2, 'msynch-'+nx+'-'+aline[ln][0], aline[ln][0])


def lines_coincidence_matrix(peakdata):
    """
    Computes a contingency matrix of how many times two lines have been synchronized

    :param peakdata:
    :return:
    """
    coinc = np.zeros((len(aline), len(aline)))

    for syn in peakdata:
        for i in syn:
            for j in syn:
                if i[0] != j[0]:
                    coinc[i[0], j[0]] += 1

    return coinc


def correlation_exp(peakdata, expcounts, window):
    """
    Computes the mutual information of the lines
    :param peakdata:
    :param expcounts:
    :return:
    """
    for _, exp in nfiles:
        #print exp
        cmatrix = lines_coincidence_matrix(peakdata[exp])
        corrmatrix = np.zeros((len(aline), len(aline)))
        for i in range(len(aline)):
            indi = aline[i][0]
            for j in range(len(aline)):
                indj = aline[j][0]
                if i != j:
                    cab = cmatrix[i, j]
                    ca = expcounts[exp][indi]
                    cb = expcounts[exp][indj]
                    tot = (ca + cb - cab) * 1.0
                    corrmatrix[i,j] = cab/tot
                    #print 'E:', exp, 'L:', indi, indj, 'C:', int(cab), ca, cb, 'Psync:', (cab/tot) #*np.log2(cab/(ca*cb))
        corrmatrix[0,0] = 1.0
        plotMatrix(corrmatrix, exp + '-W' + str(int(window*0.6))+'ms', exp + '-W'+ str(int(window*0.6))+'ms', [x for x in range(len(aline))], [x for x, _, _ in aline])
        #print '----'






nfiles = [(0, 'ctrl1'), (1, 'ctrl2'), (2, 'capsa1'), (3, 'capsa2'), (4, 'capsa3'),
         (5, 'lido1'), (6, 'lido2'), (7, 'lido3'), (8, 'lido4'), (9, 'lido5'), (10, 'lido6')
         ]

# nfiles = [(0, 'ctrl1')]

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

aline = [
         ('L4ci', 'k9.n1', 9),
         ('L4cd', 'k9.n5', 9),
        ('L5ri', 'k15.n9', 15),
        ('L5rd', 'k20.n1', 20),  #<-
        ('L5ci', 'k15.n1', 15),
        ('L5cd', 'k10.n6', 10),
        ('L6rd', 'k13.n9', 13),
        ('L6ri', 'k18.n4', 18),
        ('L6ci', 'k15.n1', 15), #<-
        ('L6cd', 'k17.n1', 17),
        ('L7ri', 'k18.n4', 18)
        ]


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
           'L7ri': (6, 1)
}

###
window = 42 / 0.6
print 'W=', int(round(window))
peakdata, expcounts = generate_synchs(aline, nfiles, window=int(round(window)))
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
length_synch_frequency_histograms(peakdata, window=int(round(window*0.6)))

### Contingency PDFs
#gen_peaks_contingency(peakdata)
