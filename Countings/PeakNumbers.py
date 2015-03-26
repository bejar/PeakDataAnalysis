"""
.. module:: PeakNumbers

PeakNumbers
*************

:Description: PeakNumbers

    

:Authors: bejar
    

:Version: 

:Created on: 16/03/2015 8:56 

"""

__author__ = 'bejar'


from config.paths import datapath, datapathnew, seqpath
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def compute_counts(window, timeline):
    bins = int(timeline[-1] / window)
    if timeline[-1] % window != 0:
        bins += 1
    res = np.zeros(bins)
    for i in range(bins):
        res[i] = len(timeline[np.logical_and(((window * i) < timeline), (timeline < ((window * i) + window)))])
    if timeline[-1] % window != 0:
        prop = (timeline[-1] % window)/window
        res[-1] = int(res[-1]/prop)

    return res

def color(i):
    if i % 2 == 0:
        return 'g'
    else:
        return 'b'

def plot_histo(accum, title, ylim):
    index = np.arange(nwin)
    bar_width = 0.5
    opacity = 0.4

    fig, ax = plt.subplots()

    for i,e in enumerate(exp):
        rects1 = plt.bar(index + (2*nwin*i* bar_width), height=accum[e], width=bar_width,
                         alpha=opacity,
                         color=color(i))

    ax.xaxis.set_ticks(np.arange(5, (nwin * 10) + 20, nwin))
    ax.set_xticklabels(exp, fontsize=24)

    fig.set_figwidth(30)
    fig.set_figheight(15)
    ax.set_ylim([0, ylim])
    plt.title(title, fontsize=48)
    fig.savefig(seqpath+'/count-' + title + '.pdf', orientation='landscape', format='pdf')


lines = ['L4cd',
         'L4ci',
         'L5cd',
         'L5rd',
         'L5ci', 'L5ri', 'L6cd', 'L6rd', 'L6ci',
         'L6ri',  'L7ri']

# lines = [#'L4cd',
#          'L5cd',
# 'L6cd', 'L6rd',
#         ]


# lines = [
#          #'L4ci',
#          'L5ci', #'L5ri',
#          'L6ci',
#          'L6ri',  #'L7ri'
# ]

# lines = ['L5ci']
exp = ['ctrl1', 'ctrl2', 'capsa1', 'capsa2', 'capsa3', 'lido1', 'lido2', 'lido3', 'lido4', 'lido5', 'lido6']

freq = 1.6  # Khz
window = 60000  # ms
cols = ['r', 'g', 'b', 'y', 'm', 'c', 'b', 'r', 'g', 'b']

dictsum = {}
for e in exp:
    dictsum[e] = {}

for line in lines:
    mattime = scipy.io.loadmat(datapathnew + '/Symbols/peaks-' + line + '.mat')
    for i, e in enumerate(exp):
        #print mattime['E{:02d}{:s}'.format(i, e)][:,1]
        dictsum[e][line] = compute_counts(window*freq, mattime['E{:02d}{:s}'.format(i, e)][:, 1])

nwin = len(dictsum[exp[0]][lines[0]])
accum = {}
maxallacum = 0
maxlineacum = 0
for e in exp:
    accum[e] = np.zeros(len(dictsum[e][lines[0]]))
    for line in lines:
        #print e, line, dictsum[e][line]
        accum[e] += dictsum[e][line]
        maxlineacum = max(maxlineacum, np.amax(dictsum[e][line]))
    maxallacum = max(np.amax(accum[e]), maxallacum)

# plot_histo(accum, 'all-I-pp'+str(window/1000)+'s', ((maxallacum //1000) + 1)*1000)
for l in lines:
    accumline = {}
    for e in exp:
        accumline[e] = dictsum[e][l]
    plot_histo(accumline, l+'-pp'+str(window/1000)+'s', ((maxlineacum //100) + 1)*100)
