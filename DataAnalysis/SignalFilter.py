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

def filterSignal(data, iband, fband, freq):
    if iband == 1:
        print fband/freq
        b,a = butter(8, fband/freq, btype='low')
        flSignal = filtfilt(b, a, data)
    elif fband == 1:
        b, a = butter(8, fband/freq, btype='high')
        flSignal = filtfilt(b, a, data)
    else:
        print iband/freq, fband/freq
        b,a = butter(8, iband/freq, btype='high')
        temp = filtfilt(b, a, data)
        b,a = butter(8, fband/freq, btype='low')
        flSignal = filtfilt(b, a, temp)
    return flSignal

from scipy.signal import butter, lfilter, iirfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=8):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


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


        for dfile in range(len(datainfo.datafiles)):
            d = f[datainfo.datafiles[dfile] + '/' + 'Raw']
            #for s in range(len(datainfo.sensors)):
            for s in [0]:
                rate = datainfo.sampling
                t = np.arange(0, 10, 1/rate)
                freq = rate * 0.5
                iband = 3.0
                fband = 10.0
                b,a = butter(2, [iband/freq, fband/freq], btype='band')
                p= filtfilt(b, a, d[:, s])
                print dfile, datainfo.sensors[s], iband, fband, np.std(p), np.std(d[:, s])
                #plt.subplots(figsize=(20, 10))
                #plot(range(p.shape[0]), p)
                #plt.show()
                # plt.title(datainfo.datafiles[dfile]+ '-' + datainfo.sensors[s], fontsize=48)
                # plt.savefig(datainfo.dpath + '/Results/' + datainfo.datafiles[dfile] + '-' + datainfo.sensors[s]
                #             + '-spectra.pdf', orientation='landscape', format='pdf')
                #plt.close()
