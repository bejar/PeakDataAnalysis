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


def resample_data(expname, wtsel, resampfac, TVD=False):
    """
    Applies a resampling of the data using Raw peaks or TVD peaks
    The time window selected has to be larger than the length of the raw peaks

    wtsel = final length to keep from the resampled window in miliseconds
    resampfac = resampling factor (times to reduce the sampling)
    :param expname:
    :param TVD:
    :return:
    """

    if TVD:
        alt = 'TVD'
    else:
        alt = ''

    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
    print datainfo.dpath + datainfo.name + '.hdf5'



    for dfile in datainfo.datafiles:
        # Sampling of the dataset in Hz / resampling factor
        resampling = f[dfile + '/Raw'].attrs['Sampling'] / resampfac

        for i, s in enumerate(datainfo.sensors):
            d = f[dfile + '/' + s + '/' + 'Peaks' + alt]

            data = d[()]

            # Number of samples in the peak
            wtlen = int(data.shape[1] / resampfac)
            wtlen_new = int(wtsel * resampling / 1000.0)
            wtdisc = int((wtlen - wtlen_new)/2.0)

            print resampling, wtlen, wtlen_new, wtdisc, data.shape[1]

            # in case we have a odd number of points in the window
            if wtlen_new + (2*wtdisc) != wtlen:
                wtdisci = wtdisc + 1
            else:
                wtdisci = wtdisc

            presamp = resample(data, wtlen, axis=1, window=wtlen*2)
            d = f.require_dataset(dfile + '/' + s + '/' +'PeaksResample' + alt, (presamp.shape[0], wtlen_new), dtype='f',
                                  data=presamp[:, wtdisci:wtlen-wtdisc], compression='gzip')
            d[()] = presamp[:, wtdisci:wtlen-wtdisc]
            f[dfile + '/' + s + '/PeaksResample' + alt].attrs['ReSampFactor'] = resampfac

    f.close()

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
#lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['130827']

for exp in lexperiments:
    resample_data(exp, 100.0, 6.0)



