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


# from pymatbridge import Matlab
#
# mlab = Matlab(executable='/home/bejar/bin/MATLAB/R2012b/bin/matlab')
#
# mlab.start()
#
# results = mlab.run_code('a=[1 2 3];')
#
# print results
#
# print mlab.get_variable('a')
#
# mlab.stop()
import scipy.io

data = {'aaa': range(10)}

scipy.io.savemat('/home/bejar/zz.mat', data, do_compression=True)

data = {'bbb': [1, 2, 3]}

scipy.io.savemat('/home/bejar/zz.mat', data, do_compression=True)

print scipy.io.whosmat('/home/bejar/zz.mat')
