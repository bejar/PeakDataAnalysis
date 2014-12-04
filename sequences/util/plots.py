"""
.. module:: plots

plots
*************

:Description: plots

    

:Authors: bejar
    

:Version: 

:Created on: 17/11/2014 13:40 

"""

__author__ = 'bejar'

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from paths import rpath

def plotSignals(signals, n, m, vmax, vmin, name, title):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(30)
    fig.set_figheight(40)
    i=1
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    for s, snm in signals:
        if min(s) != max(s):
            plotSignalValues(fig, s, n, m, i, snm, vmax, vmin)
        else:
            plotDummy(fig, len(s), n, m, i, snm)
        i += 1

    fig.suptitle(title, fontsize=48)
    fig.savefig(rpath+'/'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()
#    plt.show()


# Plot a set of signals
def plotSignalValues(fig, signal1, n, m, p, name, vmax, vmin):
    minaxis=vmin#min(signal1)
    maxaxis= vmax#max(signal1)
    num=len(signal1)
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    plt.axhline(linewidth=4, color='r', y=np.mean(signal1))
    pstd = np.std(signal1)
    plt.axhline(linewidth=4, color='b', y=np.mean(signal1)+pstd)
    plt.axhline(linewidth=4, color='b', y=np.mean(signal1)-pstd)
    sp1.plot(t,signal1)
#    plt.show()

def plotDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t,t)
#    plt.show()


def plotMatrices(matrices, n, m, name, title):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(50)
    fig.set_figheight(60)
    i=1
    plt.subplots_adjust(hspace = 0.1, wspace = 0.1)
    for s, snm in matrices:
        if s is not None:
            plotMatrixValues(fig,s,n,m,i, snm)
        else:
            plotMatrixDummy(fig,len(s),n,m,i, snm)
        i += 1

    fig.suptitle(title, fontsize=60)
    fig.savefig(rpath+'/'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()
#    plt.show()


# Plot a set of signals
def plotMatrixValues(fig, matrix, n, m, p, name):
    sp1=fig.add_subplot(n,m,p)
    plt.title(name, fontsize=48)
    sp1.imshow(matrix,  cmap=plt.cm.gray, interpolation='none')
#    plt.show()

def plotMatrixDummy(fig,num,n,m,p,name):
    minaxis=-1
    maxaxis=1
    sp1=fig.add_subplot(n,m,p)
    plt.title(name)
    sp1.axis([0,num,minaxis,maxaxis])
    t = arange(0.0, num, 1)
    sp1.plot(t,t)
#    plt.show()


def plotMatrix(matrix,name, title, ticks, lticks):
    matplotlib.rcParams.update({'font.size': 26})
    fig = plt.figure()
    fig.set_figwidth(50)
    fig.set_figheight(60)
    sp1=fig.add_subplot(1,1,1)
    plt.title(title, fontsize=48)
    img = sp1.imshow(matrix,  cmap=plt.cm.seismic, interpolation='none')
    plt.xticks(ticks, lticks, fontsize=28)
    plt.yticks(ticks, lticks, fontsize=28)
    plt.subplots_adjust(bottom=0.15)
    fig.colorbar(img, orientation='horizontal')
    fig.savefig(rpath+'/corr-'+name+'.pdf', orientation='landscape', format='pdf')
    plt.close()