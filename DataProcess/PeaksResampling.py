"""
.. module:: PeaksResampling

PeaksResampling
*************

:Description: PeaksResampling

    

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 11:41 

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


def tests1(data):
    """
    Test of resampling methods
    :return:
    """
    peak = data[1, :, 0]
    temp = rfft(peak)
    temp[5:len(temp)] = 0
    vals = irfft(temp)

    show_two_signals(peak, vals)

    res = resample(peak, 170)
    temp = rfft(res)
    temp[5:len(temp)] = 0
    vals = irfft(temp)

    show_two_signals(res, vals)

    res = decimate(peak, 6)
    temp = rfft(res)
    temp[5:len(temp)] = 0
    vals = irfft(temp)

    show_two_signals(res, vals)

    res = resample(peak, 170)
    res2 = decimate(peak, 6)

    print res.shape, res2.shape

    show_two_signals(res, res2)


def resample_data(expname):
    datainfo = experiments[expname]



    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'w')
    print datainfo.dpath + datainfo.name + '.hdf5'



    for df in datainfo.datafiles:
        mattime = scipy.io.loadmat(datainfo.dpath + df + '-peaks.mat')

        times = mattime['ipeakM']
        peaks = mattime['PeakM']
        raw = mattime['data']
        dgroup = f.create_group(df)
        dgroup.create_dataset('Raw', raw.shape, dtype='f', data=raw, compression='gzip')
        f[df + '/Raw'].attrs['Sampling'] = datainfo.sampling
        f[df + '/Raw'].attrs['Sensors'] = datainfo.sensors


        for i, s in enumerate(datainfo.sensors):
            tdata = times[:, i]
            pdata = peaks[:, :, i]

            dgroup = f.create_group(df + '/' + s)
            dgroup.create_dataset('Time', tdata[tdata != 0].shape, dtype='i', data=tdata[tdata != 0], compression='gzip')
            dgroup.create_dataset('Peaks', pdata[tdata != 0, :].shape, dtype='f', data=pdata[tdata != 0, :], compression='gzip')
            dgroup.create_dataset('PeaksResample', (pdata[tdata != 0, :].shape[0], 170), dtype='f',
                                  data=resample(pdata[tdata != 0, :], 170, axis=1), compression='gzip')

            f[df + '/' + s + '/PeaksResample'].attrs['Resampling'] = 170
    f.close()

#lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

for exp in lexperiments:
    resample_data(exp)



