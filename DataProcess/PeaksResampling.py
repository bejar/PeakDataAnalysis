"""
.. module:: PeaksResampling

PeaksResampling
*************

:Description: PeaksResampling


 Resamples the peaks from the signals and saves the results in the HDF5 files as *Signal*/PeaksResample

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 11:41 

"""

__author__ = 'bejar'

import scipy.io
from numpy.fft import rfft, irfft
from scipy.signal import resample, decimate
import h5py

from config.experiments import experiments, lexperiments
from util.plots import show_two_signals


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
            dgroup.create_dataset('Time', tdata[tdata != 0].shape, dtype='i', data=tdata[tdata != 0],
                                  compression='gzip')
            dgroup.create_dataset('Peaks', pdata[tdata != 0, :].shape, dtype='f', data=pdata[tdata != 0, :],
                                  compression='gzip')
            presamp = resample(pdata[tdata != 0, :], wsize, axis=1, window=wsize*2)
            dgroup.create_dataset('PeaksResample', (presamp.shape[0], wselect), dtype='f',
                                  data=presamp[:, wdisc:wsize-wdisc], compression='gzip')

            f[df + '/' + s + '/PeaksResample'].attrs['Resampling'] = wselect
    f.close()

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']

wsize = 250
wselect = 170
wdisc = int((wsize - wselect)/2.0)

for exp in lexperiments:
    resample_data(exp)



