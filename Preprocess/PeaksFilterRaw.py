"""
.. module:: PeaksFilterRaw

PeaksFilterRaw
*************

:Description: PeaksFilterRaw

 Filters the signals with a band-pass butterworth filter and saves the filtered signals
  and the identified peaks extracted from the filtered signal

:Authors: bejar
    

:Version: 

:Created on: 13/07/2015 8:37 

"""

__author__ = 'bejar'


from scipy.signal import decimate
from scipy.signal import butter, filtfilt, freqs, lfilter
import h5py

from config.experiments import experiments, lexperiments
import numpy as np

from util.plots import show_signal, plotSignals, show_two_signals


def filter_data(expname, iband, fband):
    """
    Filters and saves the raw signal in the datafile

    :param expname:
    :param iband:
    :param fband:
    :return:
    """
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
    print datainfo.dpath + datainfo.name + '.hdf5'
    wtime = 120e-3 # Window length in miliseconds
    sampling = datainfo.sampling #/ 6.0
    Tw = int(2 * np.round(wtime*sampling/2))

    for df in datainfo.datafiles:
        print df
        d = f[df + '/Raw']
        samp = f[df + '/Raw'].attrs['Sampling']
        data = d[()]
        freq = samp * 0.5
        b, a = butter(3, [iband/freq, fband/freq], btype='band')
        filtered = np.zeros(data.shape)
        for i in range(data.shape[1]):
            filtered[:, i] = filtfilt(b, a, data[:, i])
        d = f.require_dataset(df + '/RawFiltered', filtered.shape, dtype='f', data=filtered, compression='gzip')
        d[()] = filtered
        f[df + '/RawFiltered'].attrs['Low'] = iband
        f[df + '/RawFiltered'].attrs['high'] = fband
        for s in datainfo.sensors:
            i = datainfo.sensors.index(s)
            times = f[df + '/' + s + '/TimeClean']
            rawpeaks = np.zeros((times.shape[0], Tw))
            print times.shape[0]
            for j in range(times.shape[0]):
                tstart = times[j] - np.floor(Tw / 2)
                tstop = tstart + Tw
                if tstart > 0 and tstop < filtered.shape[0]:
                    rawpeaks[j, :] = filtered[tstart:tstop, i]
                elif tstart < 0:
                    rawpeaks[j, :] = np.hstack((np.zeros(np.abs(tstart)), filtered[0:tstop, i]))
                else:
                    rawpeaks[j, :] = np.hstack((filtered[tstart:tstop, i], np.zeros(tstop-filtered.shape[0])))
           #show_signal(rawpeaks[j])
            # Peak Data
            dfilter = f[df + '/' + s]
            #del dfilter['PeaksFilter']
            dfilter.require_dataset('PeaksFilter', rawpeaks.shape, dtype='f', data=rawpeaks,
                                      compression='gzip')



    f.close()


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

lexperiments = ['e150514']
for exp in lexperiments:
    filter_data(exp, 1.0, 200.0)
