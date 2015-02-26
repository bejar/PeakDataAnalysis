"""
.. module:: TestABF

TestABF
*************

:Description: TestABF

    

:Authors: bejar
    

:Version: 

:Created on: 12/12/2014 8:19 

"""

__author__ = 'bejar'

from neo.io import AxonIO
import numpy as np
from config.paths import datapath2
import scipy.io

datafiles = [(['e130716f00-cntrl1', 'e130716f02-cntrl2', 'e130716f03-cntrl3'], 12, 10204.1),
             (['e130827f23-cntrl1', 'e130827f26-cntrl2', 'e130827f37-cntrl3'], 11, 10256.4),
             (['e130903f20-cntrl1', 'e130903f22-cntrl2', 'e130903f25-cntrl3'], 11, 10256.4),
             (['e141113f09-cntrl1', 'e141113f11-cntrl2', 'e141113f13-cntrl3'], 12, 10204.1),
             (['e141029f35-cntrl1', 'e141029f37-cntrl2', 'e141029f39-cntrl3'], 12, 10204.1),
             (['e141016f07-cntrl1', 'e141016f09-cntrl2', 'e141016f11-cntrl3'], 12, 10204.1),
             (['e140911f20-cntrl1', 'e140911f33-cntrl2', 'e140911f36-cntrl3'], 12, 10416.7),
             (['e140311f09-cntrl1', 'e140311f13-cntrl2', 'e140311f23-cntrl3'], 12, 10204.1),
             (['e140225f31-cntrl1', 'e140225f34-cntrl2', 'e140225f39-cntrl3', 'e140225f47-cntrl4', 'e140225f50-cntrl5', 'e140225f59-cntrl6'], 12, 10204.1),
             (['e140220f8-ctrl1', 'e140220f10-ctrl2', 'e140220f12-ctrl3'], 12, 10416.7),
             ]

for dataf, nsig, _ in datafiles:
    for files in dataf:
        print 'Reading: ', files, '...'
        data = AxonIO(datapath2 + files + '.abf')

        bl = data.read_block(lazy=False, cascade=True)

        dim = bl.segments[0].analogsignals[0].shape[0]

        matrix = np.zeros((dim, nsig))
        # for sig in bl.segments[0].analogsignals:
        #     i += 1
        #     #print sig.duration, sig.signal, len(sig.times), i
        #     print sig.name, sig.units, sig.sampling_rate, sig.dtype, sig.duration, sig.shape


        for i in range(dim):
            for j in range(nsig):
                matrix[i][j] = bl.segments[0].analogsignals[j][i].magnitude

        peakdata = {'data': matrix}
        print 'Saving: ', files, '...'
        scipy.io.savemat(datapath2 + files + '.mat', peakdata, do_compression=True)
