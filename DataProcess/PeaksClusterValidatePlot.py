"""
.. module:: PeaksClusterStabilityPlot

PeaksClusterStabilityPlot
*************

:Description: PeaksClusterStabilityPlot

    Plots the curve of stability measure for different number of clusters

:Authors: bejar
    

:Version: 

:Created on: 02/03/2015 7:09 

"""

__author__ = 'bejar'

import matplotlib.pyplot as plt
from pylab import *
from config.experiments import experiments, lexperiments


def plot_cluster_validation(exp):
    datainfo = experiments[exp]

    nfile = open(datainfo.dpath + '/Results/' + datainfo.name + '-val-whole.txt', 'r')
    alldata = nfile.readlines()
    nfile.close()

    line = 1
    nsig = 1
    fig = plt.figure()
    while line < len(alldata):
        cline = alldata[line].split(' ')
        signal = cline[1]
        print signal
        numc = []
        valc = []
        line += 1
        cline = alldata[line].split(' ')
        while cline[0] != 'S=' and line < len(alldata):
            numc.append(int(cline[0]))
            valc.append(float(cline[2]))
            line += 1
            if line < len(alldata):
                cline = alldata[line].split(' ')
        line += 2
        ax = fig.add_subplot(6, 2, nsig)
        xis = ax.axis([4, np.max(numc), 0.5, 1])
        plt.xticks(np.arange(4, np.max(numc) + 1, 2))
        ax.text(6, 0.9, signal)
        ax.plot(numc, valc)
        plt.title(datainfo.name)
        nsig += 1
    fig.set_figwidth(15)
    fig.set_figheight(30)
    fig.savefig(datainfo.dpath  + '/Results/' + datainfo.name + '-cluster-val.pdf', orientation='landscape', format='pdf')


# --------------------------------------
lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e141016', 'e140911', 'e140220', 'e130827', 'e140225']

for exp in lexperiments:
    plot_cluster_validation(exp)

