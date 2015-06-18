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

from config.experiments import experiments, lexperiments
from util.plots import show_two_signals


def save_data(expname, ext=""):

    datainfo = experiments[expname]
    print datainfo.dpath + datainfo.name + ext + '.hdf5'

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')

    for dfile in datainfo.datafiles:
        print datainfo.dpath + dfile + ext + '-IFP.mat'
        mattime = scipy.io.loadmat(datainfo.dpath + dfile + ext + '-IFP.mat')
        raw = mattime['data']
        d = f.require_dataset(dfile + '/IFP', raw.shape, dtype='f', data=raw, compression='gzip')
        d[()] = raw

    f.close()

# ----------------------------------------------------------------------------------------------

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

#lexperiments = ['e130827', 'e140225', 'e140220', 'e141016', 'e140911']
lexperiments = ['e140515']

for exp in lexperiments:
    save_data(exp, ext='')
