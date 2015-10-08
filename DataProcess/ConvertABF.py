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
import scipy.io

from config.paths import cinvesdata, cinvesdatanew

datafiles = [(['14304g08', '14304g12',  '14304g23', '14304g32', '14304g34', '14304g39',
               '14304g43','14304g53',  '14304g55', '14304g57', '14304g58', '14304g61',
               '14304g69', '14304g73'], 12, 2014.0)
             ]





# datafiles = [(['15514027'],
#               12, 10000.0)]

for dataf, nsig, _ in datafiles:
    for files in dataf:
        print 'Reading: ', files, '...'
        data = AxonIO(cinvesdatanew + 'e140304/' + files + '.abf')

        bl = data.read_block(lazy=False, cascade=True)

        dim = bl.segments[0].analogsignals[0].shape[0]

        print dim
        matrix = np.zeros((nsig, dim))
        # for sig in bl.segments[0].analogsignals:
        # i += 1
        #     #print sig.duration, sig.signal, len(sig.times), i
        #     print sig.name, sig.units, sig.sampling_rate, sig.dtype, sig.duration, sig.shape


        for j in range(nsig):
            matrix[j][:] = bl.segments[0].analogsignals[j][:].magnitude

        peakdata = {'data': matrix.T}
        print 'Saving: ', files, '...'
        scipy.io.savemat(cinvesdata + files + '.mat', peakdata, do_compression=True)

