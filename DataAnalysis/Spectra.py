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
from scipy.signal import  decimate

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter

if __name__ == '__main__':
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
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

        for dfile in range(0,len(datainfo.datafiles)):
            d = f[datainfo.datafiles[dfile] + '/' + 'Raw']
            print d.shape
            for s in range(len(datainfo.sensors)):
                print dfile, datainfo.sensors[s]
                rate = 10000.0
                t = np.arange(0, 10, 1/rate)
                x = d[0:6100000, s]
                p = np.abs(np.fft.rfft(x))**2
                spec = np.linspace(0, (rate)/2, len(p))
                #p = decimate(p,20)
                plt.subplots(figsize=(20, 10))
                plot(spec[0:12000], p[0:12000])
                plt.title(datainfo.datafiles[dfile]+ '-' + datainfo.sensors[s], fontsize=48)
                plt.savefig(datainfo.dpath + '/Results/' + datainfo.datafiles[dfile] + '-' + datainfo.sensors[s]
                            + '-spectra.pdf', orientation='landscape', format='pdf')
                plt.close()
