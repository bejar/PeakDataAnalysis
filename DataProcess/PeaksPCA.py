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

def compute_pca_basal_transformation(expname, components=10, baseline=40, TVD=False):
    """
    Transforms the data reconstructing the peaks using some components of the PCA
    and uses the mean of the baseline points to move the peak

    :param components: Components selected from the PCA
    :param baseline: Points to use to move the peak
    :return:
    """

    if TVD:
        alt = ''
    else:
        alt = 'TVD'

    lind = range(baseline)
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

    for dfile in datainfo.datafiles:
        for s in datainfo.sensors:
            d = f[dfile + '/' + s + '/' + 'PeaksResample' + alt]
            data = d[()]
            # Substract the basal
            # for row in range(data.shape[0]):
            #     vals = data[row, lind]
            #     basal = np.mean(vals)
            #     data[row] -= basal

            pca = PCA(n_components=data.shape[1])
            res = pca.fit_transform(data)
            res[:, components:] = 0
            trans = pca.inverse_transform(res)

            # Substract the basal
            for row in range(trans.shape[0]):
                vals = trans[row, lind]
                basal = np.mean(vals)
                trans[row] -= basal


            # show_signal(trans[0, :])
            print dfile + '/' + s + '/' +'PeaksResamplePCA'+alt
            d = f.require_dataset(dfile + '/' + s + '/' +'PeaksResamplePCA'+alt, trans.shape, dtype='f',
                              data=trans, compression='gzip')
            d[()] = trans


# ---------------------------------------------------------------------------------------------------------------

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

# Good experiments
lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

#lexperiments = ['e130827']
for expname in lexperiments:
    compute_pca_basal_transformation(expname)
