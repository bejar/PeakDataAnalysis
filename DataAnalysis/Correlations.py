"""
.. module:: Correlations

Correlations
*************

:Description: Correlations

    

:Authors: bejar
    

:Version: 

:Created on: 09/06/2015 8:29 

"""

__author__ = 'bejar'

import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter

if __name__ == '__main__':

    lexperiments = ['e140515']

    TVD = False
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]
        f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')

        for dfile in datainfo.datafiles:
            print dfile
            d = f[dfile + '/' +'Raw']
            corrmat = np.corrcoef(d, rowvar=0)
            # corrmat[0,0] = 0
            # corrmat[d.shape[1]-1,d.shape[1]-1] = 1

            fig = plt.figure()
            sp1 = fig.add_subplot(1, 1, 1)
            img = sp1.imshow(corrmat, cmap=plt.cm.seismic, interpolation='none')
            ticks = [x for x in range(len(datainfo.sensors))]
            lticks = [x for x in datainfo.sensors]
            plt.xticks(ticks, lticks, fontsize=10)
            plt.yticks(ticks, lticks, fontsize=10)

            fig.colorbar(img, orientation='horizontal')

            #plt.show()
            fig.savefig(datainfo.dpath + '/Results/' + dfile + '.pdf', orientation='landscape', format='pdf')
            np.savetxt(datainfo.dpath + '/Results/' + dfile + '.csv', corrmat, fmt='%.18e', delimiter=',', newline='\n')
