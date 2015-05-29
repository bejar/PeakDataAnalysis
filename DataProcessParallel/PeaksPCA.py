"""
.. module:: PeaksPCA

PeaksPCA
*************

:Description: PeaksPCA

    Performs a PCA of the peaks and reconstructs them with only a number of them.
    After, it removes the mean a subwidow of the initial and final values of the signal
    Eventually saves the peaks in *Signal*/PeaksPCA

:Authors: bejar
    

:Version: 

:Created on: 26/03/2015 7:52 

"""

__author__ = 'bejar'

import h5py
from sklearn.decomposition import PCA
import numpy as np

from config.experiments import experiments
from util.plots import show_signal
from joblib import Parallel, delayed

def do_the_job(dfile, sensor, components, lind, alt):
    """
    Transforms the data reconstructing the peaks using some components of the PCA
    and uses the mean of the baseline points to move the peak

    :param dfile: datafile
    :param sensor: sensor
    :param alt: alternative data
    :param components: Components selected from the PCA
    :param lind: Points to use to move the peak
    :return:
    """
    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    d = f[dfile + '/' + sensor + '/' + 'PeaksResample' + alt]
    data = d[()]

    pca = PCA(n_components=data.shape[1])
    res = pca.fit_transform(data)
    res[:, components:] = 0
    trans = pca.inverse_transform(res)

    # Substract the basal
    for row in range(trans.shape[0]):
        vals = trans[row, lind]
        basal = np.mean(vals)
        trans[row] -= basal

    f.close()
    return trans

# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    lexperiments = ['e130716']

    TVD = False
    baseline = 40
    components = 10
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        lind = range(baseline)
        datainfo = experiments[expname]


        for dfile in datainfo.datafiles:
            print dfile
            # Paralelize PCA computation
            res = Parallel(n_jobs=-1)(delayed(do_the_job)(dfile, s, components, lind, alt) for s in datainfo.sensors)
            print 'Parallelism ended'
            # Save all the data
            f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')
            for trans, sensor in zip(res, datainfo.sensors):
                print dfile + '/' + sensor + '/' + 'PeaksResamplePCA' + alt
                d = f.require_dataset(dfile + '/' + sensor + '/' + 'PeaksResamplePCA' + alt, trans.shape, dtype='f', data=trans, compression='gzip')
                d[()] = trans

            f.close()
