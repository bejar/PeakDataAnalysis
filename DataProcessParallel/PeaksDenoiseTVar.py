"""
.. module:: PeaksDenoiseTVar

PeaksDenoiseTVar
*************

:Description: PeaksDenoiseTVar

    Denoise data using Total Variance Denoising

:Authors: bejar
    

:Version: 

:Created on: 28/05/2015 9:32 

"""


__author__ = 'bejar'

import h5py
import numpy as np

from config.experiments import experiments
from util.plots import show_signal
import util.TotalVariation as tv
from joblib import Parallel, delayed


def do_the_job(sensor, dfile, lratio):
    """
    Performs Total Variation Denoising of the raw peaks

    :param expname:
    :param lratio:  Ratio for the regularization  - The higher the flatter is the signal
    :return:
    """
    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    d = f[dfile + '/' + sensor + '/' + 'Peaks']
    data = d[()]

    datares = np.zeros(data.shape)

    for i in range(data.shape[0]):
        x = data[i].reshape((data[i].shape[0]), 1)
        lmax = tv.tvdiplmax(x)
        y, _, _, _ = tv.tvdip(x, lmax*lratio, False, 1e-5)
        datares[i] = y[:, 0]
    f.close()
    return datares

# -----------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']
    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']
    lexperiments = ['e130716']

    for expname in lexperiments:
        datainfo = experiments[expname]
        for dfile in datainfo.datafiles:
            print dfile
            # Paralelize PCA computation
            res = Parallel(n_jobs=-1)(delayed(do_the_job)(s, dfile, np.array([2e-2])) for s in datainfo.sensors)
            print 'Parallelism ended'

            # Save all the data
            f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
            for datares, sensor in zip(res, datainfo.sensors):
                print dfile + '/' + sensor + '/' + 'PeaksTVD'
                d = f.require_dataset(dfile + '/' + sensor + '/' + 'PeaksTVD', datares.shape, dtype='f',
                                      data=datares, compression='gzip')
                d[()] = datares

            f.close()
