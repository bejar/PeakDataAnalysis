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
from pylab import *

from config.paths import datapath, seqpath


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
    fig.savefig(seqpath+'/icons/'+line+'.cl'+str(nc)+'.png', orientation='landscape',format='png', pad_inches=0.1)


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

# line = 'L6ri'
# clust = '.k15.n1'

for line, clust, _ in aline:
    matpeaks = scipy.io.loadmat(datapath + 'Selected/centers.' + line + '.' + clust + '.mat')


    clpeaks = matpeaks['C']

    print clpeaks.shape

    peakLength = clpeaks.shape[1]

    for i in range( clpeaks.shape[0]):
        plotSignalValues(clpeaks[i], i+1)

