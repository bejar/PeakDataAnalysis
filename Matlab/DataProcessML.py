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


datafiles = [(['e130716f00-cntrl1', 'e130716f02-cntrl2', 'e130716f03-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e130827f23-cntrl1', 'e130827f26-cntrl2', 'e130827f37-cntrl3'], 11,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri'],
              10256.4),
             (['e130903f20-cntrl1', 'e130903f22-cntrl2', 'e130903f25-cntrl3'], 11, 10256.4),
              ['L4ri', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci'],
             (['e141113f09-cntrl1', 'e141113f11-cntrl2', 'e141113f13-cntrl3'], 12, 10204.1),
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
             (['e141029f35-cntrl1', 'e141029f37-cntrl2', 'e141029f39-cntrl3'], 12, 10204.1),
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
             (['e141016f07-cntrl1', 'e141016f09-cntrl2', 'e141016f11-cntrl3'], 12, 10204.1),
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
             (['e140911f20-cntrl1', 'e140911f33-cntrl2', 'e140911f36-cntrl3'], 12, 10416.7),
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
             (['e140311f09-cntrl1', 'e140311f13-cntrl2', 'e140311f23-cntrl3'], 12, 10204.1),
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
             (['e140225f31-cntrl1', 'e140225f34-cntrl2', 'e140225f39-cntrl3', 'e140225f47-cntrl4', 'e140225f50-cntrl5',
               'e140225f59-cntrl6'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e140220f8-ctrl1', 'e140220f10-ctrl2', 'e140220f12-ctrl3'], 12,
              ['DRP', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci', 'L7ri'],
              10416.7),
             ]



mlab = Matlab(executable='/home/bejar/bin/MATLAB/R2014b/bin/matlab')

mlab.start()


for files, nsig, singals, sampling in datafiles:
    for file in files:
        print 'Processing ', file
        nfile = '/home/bejar/Data/Cinvestav/' + file + '.mat'
        nfiler = '/home/bejar/Data/Cinvestav/' + file + '-peaks.mat'
        mlab.run_code('cdp_identification(\'file\', \'nfiler\', 100e-3,' + str(sampling) + ')')

mlab.stop()


# print results
# print mlab.get_variable('a')

#res = mlab.run_func('jk.m', {'arg1': 3, 'arg2': 5})
