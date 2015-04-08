"""
.. module:: ResTest

ResTest
*************

:Description: ResTest

    

:Authors: bejar
    

:Version: 

:Created on: 25/03/2015 14:40 

"""

__author__ = 'bejar'


from config.paths import cinvesdata
from config.experiments import experiments
from util.Experiment import Experiment
from util.plots import show_signal, show_two_signals
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import rfft, irfft
from scipy.signal import resample, decimate
import h5py

def printing(name, object):
    if type(object) == h5py._hl.dataset.Dataset and 'Time' in name:
        print name, object.shape

expname = 'e130827'#'e130716'#'e130903'#

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

# for s in datainfo.sensors:
#     d = f[datainfo.datafiles[0] + '/' + s + '/' + 'Peaks']
#     print d.shape
#     show_signal(d[0, :])

f.visititems(printing)