"""
.. module:: MAtlabtest

MAtlabtest
*************

:Description: MAtlabtest

    

:Authors: bejar
    

:Version: 

:Created on: 26/01/2015 9:55 

"""

__author__ = 'bejar'


from pymatbridge import Matlab
from config.experiments import experiments, lexperiments


#lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225', 'e140220']
lexperiments = ['e130716']

mlab = Matlab(executable='/home/bejar/bin/MATLAB/R2014b/bin/matlab')

mlab.start()
a = mlab.run_code('cd(\'/home/bejar/PycharmProjects/PeakDataAnalysis/Matlab/\')')
print a

datasufix = '-RawResampled'

for expname in lexperiments:
    datainfo = experiments[expname]
    sampling = datainfo.sampling /6.0

    for file in datainfo.datafiles:
        nfile = '/home/bejar/Data/Cinvestav/' + file + datasufix + '.mat'
        nfiler = '/home/bejar/Data/Cinvestav/' + file + datasufix + '-peaks.mat'
        print 'Processing ', file
        print 'IN= ', nfile
        print 'OUT= ', nfiler
        a = mlab.run_code('cdp_identification(\'' + nfile + '\', \'' + nfiler + '\', 100e-3,' + str(sampling) + ')')
        print '************************************************'

mlab.stop()


# print results
# print mlab.get_variable('a')

#res = mlab.run_func('jk.m', {'arg1': 3, 'arg2': 5})
