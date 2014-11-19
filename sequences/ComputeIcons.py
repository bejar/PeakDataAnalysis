"""
.. module:: ComputeIcons

ComputeIcons
*************

:Description: ComputeIcons

    

:Authors: bejar
    

:Version: 

:Created on: 20/10/2014 9:09 

"""

__author__ = 'bejar'

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


def plotSignalValues(signals, nc):
    fig = plt.figure()
    minaxis=-0.1
    maxaxis=0.3
    sp1=fig.add_subplot(1,1,1)
    sp1.axis([0,peakLength,minaxis,maxaxis])

    sp1.axes.get_xaxis().set_visible(False)
    sp1.axes.get_yaxis().set_visible(False)

    t = arange(0.0, peakLength, 1)
    sp1.plot(t, signals, 'r')
    fig.set_figwidth(1.5)
    fig.set_figheight(1.5)

    #plt.show()
    fig.savefig(ipath+'/'+line+'.cl'+str(nc)+'.png', orientation='landscape',format='png', pad_inches=0.1)

line = 'L6ri'
clust = '.k15.n1'


cpath = '/home/bejar/Dropbox/Filtro Rudomin/Estability/'
rpath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/'
ipath = '/home/bejar/Documentos/Investigacion/cinvestav/secuencias/icons/'
ocpath = '/home/bejar/Documentos/Investigacion/cinvestav/'

matpeaks = scipy.io.loadmat(ocpath + '/centers.' + line + clust + '.mat')


clpeaks = matpeaks['C']

print clpeaks.shape

peakLength = clpeaks.shape[1]

for i in range( clpeaks.shape[0]):
    plotSignalValues(clpeaks[i], i+1)

