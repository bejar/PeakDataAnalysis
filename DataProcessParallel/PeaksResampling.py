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
from joblib import Parallel, delayed


def do_the_job(dfile, sensor, wtsel, resampfac, alt, ext="", filter=False):
    """
    Applies a resampling of the data using Raw peaks or TVD peaks
    The time window selected has to be larger than the length of the raw peaks

    wtsel = final length to keep from the resampled window in miliseconds
    resampfac = resampling factor (times to reduce the sampling)
    :param expname:
    :param TVD:
    :return:
    """

    print datainfo.dpath + datainfo.name + ext + '.hdf5', sensor
    f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r')

    # Sampling of the dataset in Hz / resampling factor
    resampling = f[dfile + '/Raw'].attrs['Sampling'] / resampfac

    if filter:
        d = f[dfile + '/' + sensor + '/' + 'PeaksFilter' + alt]
    else:
        d = f[dfile + '/' + sensor + '/' + 'Peaks' + alt]

    data = d[()]

    # Number of samples in the peak
    wtlen = int(data.shape[1] / resampfac)
    wtlen_new = int(wtsel * resampling / 1000.0)
    wtdisc = int((wtlen - wtlen_new)/2.0)
    presamp = resample(data, wtlen, axis=1, window=wtlen*2)

    f.close()

    # in case we have a odd number of points in the window
    if wtlen_new + (2*wtdisc) != wtlen:
        wtdisci = wtdisc + 1
    else:
        wtdisci = wtdisc
    return presamp[:, wtdisci:wtlen-wtdisc]

# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':


    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
    #lexperiments = ['e130827']  # ['e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
    lexperiments = ['e130827', 'e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e150514']

    ext = ''
    TVD = False
    if TVD:
        alt = 'TVD'
    else:
        alt = ''

    wtsel = 100.0
    resampfactor = 6.0
    for expname in lexperiments:

        datainfo = experiments[expname]

        for dfile in datainfo.datafiles:
            print dfile
            # Paralelize PCA computation
            res = Parallel(n_jobs=-1)(delayed(do_the_job)(dfile, s, wtsel, resampfactor, alt, ext, filter=True) for s in datainfo.sensors)
            #print 'Parallelism ended'

            f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')
            for presamp, sensor in zip(res, datainfo.sensors):
                print dfile + '/' + sensor + '/' + 'PeaksResample' + alt
                if dfile + '/' + sensor + '/' + 'PeaksResample' in f:
                    del f[dfile + '/' + sensor + '/' + 'PeaksResample']
                d = f.require_dataset(dfile + '/' + sensor + '/' + 'PeaksResample', presamp.shape, dtype='f',
                                      data=presamp, compression='gzip')
                d[()] = presamp
                f[dfile + '/' + sensor + '/PeaksResample' + alt].attrs['ReSampFactor'] = resampfactor

            f.close()
