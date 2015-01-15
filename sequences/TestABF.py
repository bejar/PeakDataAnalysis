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
from util.paths import dpath



data = AxonIO(dpath+'e130716f00-cntrl1.abf')

bl = data.read_block(lazy=False, cascade=True)

i = 0
for sig in bl.segments[0].analogsignals:
    i += 1
    #print sig.duration, sig.signal, len(sig.times), i
    print sig.name, sig.units, sig.sampling_rate, sig.dtype, sig.duration, sig.shape

i = 0

for sig in bl.segments[0].analogsignals:
    i += 1
    #print sig.duration, sig.signal, len(sig.times), i
    print sig[0].magnitude
