"""
.. module:: Spectra

Spectra
*************

:Description: Spectra

    

:Authors: bejar
    

:Version: 

:Created on: 11/06/2015 11:38 

"""
from __future__ import division

__author__ = 'bejar'


import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *
from scipy.signal import decimate, butter, filtfilt, freqs, lfilter

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter
from util.STFT import stft
import seaborn as sns

if __name__ == '__main__':
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']e140515
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
        f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')
        chunk = 2000000

        rate = datainfo.sampling
        for dfile in [0]:#range(len(datainfo.datafiles)):
            d = f[datainfo.datafiles[dfile] + '/' + 'RawFiltered']
            print d.shape, datainfo.sampling/2
            for s in range(len(datainfo.sensors)):
                print dfile, datainfo.sensors[s]
                length = int(rate)
                over = 2
                vec = stft(d[0:chunk, s], length, over)
                print vec.shape
                fig = plt.figure()
                fig.set_figwidth(100)
                fig.set_figheight(20)

                sp1 = fig.add_subplot(1, 1, 1)
                img = sp1.imshow(vec[:,0:100].T, cmap=plt.cm.seismic, interpolation='none')
                fig.savefig(datainfo.dpath + '/Results/' + datainfo.datafiles[dfile] + '-' + datainfo.sensors[s]
                            + '-ftft.pdf', orientation='landscape', format='pdf')
                #plt.show()
                plt.close()
