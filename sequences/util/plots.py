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
    plt.subplots_adjust(hspace = 0.5, wspace = 0.3)
    for s,snm in signals:
        if min(s)!=max(s):
            plotSignalValues(fig,s,n,m,i,snm, vmax, vmin)
        else:
            plotDummy(fig,len(s),n,m,i,snm)
        i += 1

    fig.suptitle(title, fontsize=48)
    fig.savefig(rpath+'/'+name+'.png', orientation='landscape', format='png')
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
