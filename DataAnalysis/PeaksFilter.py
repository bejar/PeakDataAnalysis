"""
.. module:: PeaksCreateHDFS

PeaksCreateHDF
*************

:Description: PeaksCreateHDF

 Generates a HDF5 file with the raw data and the information of the extracted peaks

:Authors: bejar
    

:Version: 

:Created on: 28/05/2015 12:58 

"""

__author__ = 'bejar'

import scipy.io
from numpy.fft import rfft, irfft
from scipy.signal import resample, decimate
import h5py
import numpy as np
from scipy.signal import decimate, butter, filtfilt, freqs, lfilter

from config.experiments import experiments, lexperiments
from util.plots import show_two_signals

def filterSignal(data, iband, fband, freq):
    if iband == 1:
        b,a=scipy.signal.butter(8,fband/freq, btype='low')
        flSignal=scipy.signal.filtfilt(b, a, data)
    else:
        b,a=scipy.signal.butter(8,iband/freq, btype='high')
        temp=scipy.signal.filtfilt(b, a, data)
        b,a=scipy.signal.butter(8,fband/freq, btype='low')
        flSignal=scipy.signal.filtfilt(b, a, temp)
    return flSignal


def save_data(expname, ext=""):

    datainfo = experiments[expname]
    print datainfo.dpath + datainfo.name + ext + '.hdf5'

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')
    b, a = butter(4, 1.0/(datainfo.sampling*0.5), btype='high')

    for dfile in datainfo.datafiles:
        print dfile
        raw = f[dfile + '/' + 'Raw']
        filter = np.zeros(raw.shape)
        for i in range(len(datainfo.sensors)):
            filter[:, i] = filtfilt(b, a, raw[:, i])
        d = f.require_dataset(dfile + '/RawFilter', filter.shape, dtype='f', data=filter, compression='gzip')
        d[()] = filter

    f.close()

# ----------------------------------------------------------------------------------------------

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

#lexperiments = ['e130827', 'e140225', 'e140220', 'e141016', 'e140911']
lexperiments = ['e140515']

for exp in lexperiments:
    save_data(exp, ext='')
