"""
.. module:: PeaksClustering

PeaksClustering
*************

:Description: PeaksClustering

    

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 8:10 

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
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

expname = 'e130716f00'

datainfo = experiments[expname]

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

for s in datainfo.sensors:
    d = f[datainfo.datafiles[0] + '/' + s + '/' + 'PeaksPCA']
    km = KMeans(n_clusters=10)
    data = d[()]

