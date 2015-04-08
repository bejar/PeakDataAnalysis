"""
.. module:: PeaksWholeResampling

PeaksWholeResampling
*************

:Description: PeaksWholeResampling

    

:Authors: bejar
    

:Version: 

:Created on: 07/04/2015 11:03 

"""

__author__ = 'bejar'


from config.paths import cinvesdata
from config.experiments import experiments, lexperiments
from util.Experiment import Experiment
from util.plots import show_signal, show_two_signals
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, irfft
from scipy.signal import resample, decimate
import h5py

resampling = 6

def resample_data(expname):
    datainfo = experiments[expname]


    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
    print datainfo.dpath + datainfo.name + '.hdf5'


    for df in datainfo.datafiles:
        print f[df + '/Raw'].shape
        d = f[df + '/Raw']
        samp = f[df + '/Raw'].attrs['Sampling']

        data = d[()]
        datasampled = decimate(data, resampling, axis=0)
        print datasampled.shape
        d = f[df]
        d.create_dataset('RawResampled', datasampled.shape, dtype='f', data=datasampled, compression='gzip')
        f[df + '/RawResampled'].attrs['Sampling'] = float(samp / resampling)

    f.close()


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

for exp in lexperiments:
    resample_data(exp)

