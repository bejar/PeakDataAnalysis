"""
.. module:: PeaksCheckValues

PeaksCheckValues
*************

:Description: PeaksCheckValues

    Prints various statistical information for the datasets

:Authors: bejar
    

:Version: 

:Created on: 06/05/2015 13:34 

"""

__author__ = 'bejar'



import h5py
import numpy as np
from config.experiments import experiments


def printing(name, object):
    if type(object) == h5py._hl.dataset.Dataset and 'Time' in name:
        print name, object.shape


lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']
#lexperiments = ['e130716']
for expname in lexperiments:
    print '########################'
    print 'Experiment:', expname
    datainfo = experiments[expname]

    f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r')

    files = datainfo.datafiles
    for file in files:
        print '++++++++++++++++++++++++++++'
        print 'FILE:', file
        d = f[file + '/Raw']
#        print d.shape[0], 'MX=', np.max(d), 'MN=', np.min(d), 'MD=', np.mean(d), 'ST=', np.std(d)
        for s in datainfo.sensors:
            if s[0] == 'L':
                d = f[file + '/' + s + '/' + 'Peaks']
                print s, d.shape[0], np.max(d), np.min(d), np.std(d), np.mean(d)


