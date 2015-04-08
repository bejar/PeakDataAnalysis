"""
.. module:: PeaksExtractData

PeaksExtractData
*************

:Description: PeaksExtractData

    

:Authors: bejar
    

:Version: 

:Created on: 07/04/2015 13:38 

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


def extract_data(expname, dataset):
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')
    print datainfo.dpath + datainfo.name + '.hdf5'


    for df in datainfo.datafiles:
        print f[df + '/' + dataset].shape
        d = f[df + '/' + dataset]

        data = d[()]
        matdata={}
        matdata['data'] = data
        scipy.io.savemat(datainfo.dpath + '/' + df + '-' + dataset, matdata,do_compression=True)

    f.close()

#lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e130716']

for exp in lexperiments:
    extract_data(exp, 'RawResampled')
