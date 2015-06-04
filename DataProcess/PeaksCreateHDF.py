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

    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'w')

    for dfiles in datainfo.datafiles:
        print datainfo.dpath + dfiles + ext + '-peaks.mat'
        mattime = scipy.io.loadmat(datainfo.dpath + dfiles + ext + '-peaks.mat')

        times = mattime['ipeakM']
        peaks = mattime['PeakM']
        raw = mattime['data']
        dgroup = f.create_group(dfiles)
        dgroup.create_dataset('Raw', raw.shape, dtype='f', data=raw, compression='gzip')
        f[dfiles + '/Raw'].attrs['Sampling'] = datainfo.sampling
        f[dfiles + '/Raw'].attrs['Sensors'] = datainfo.sensors

        for i, s in enumerate(datainfo.sensors):
            print s,
            tdata = times[:, i]
            pdata = peaks[:, :, i]

            dgroup = f.create_group(dfiles + '/' + s)
            # Time of the peak
            dgroup.create_dataset('Time', tdata[tdata != 0].shape, dtype='i', data=tdata[tdata != 0],
                                  compression='gzip')
            # Peak Data
            dgroup.create_dataset('Peaks', pdata[tdata != 0, :].shape, dtype='f', data=pdata[tdata != 0, :],
                                  compression='gzip')
        print
    f.close()

# ----------------------------------------------------------------------------------------------

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

#lexperiments = ['e130827', 'e140225', 'e140220', 'e141016', 'e140911']
lexperiments = ['e140515b']

for exp in lexperiments:
    save_data(exp, ext='')
