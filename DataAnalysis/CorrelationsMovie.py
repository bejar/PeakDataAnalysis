"""
.. module:: Correlations

Correlations
*************

:Description: Correlations

    

:Authors: bejar
    

:Version: 

:Created on: 09/06/2015 8:29 

"""

__author__ = 'bejar'

import h5py
from util.plots import show_signal, plotSignals
from util.distances import simetrized_kullback_leibler_divergence, square_frobenius_distance, renyi_half_divergence, \
    jensen_shannon_divergence, bhattacharyya_distance, hellinger_distance
import numpy as np
from sklearn.cluster import KMeans
from pylab import *

from config.experiments import experiments
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from operator import itemgetter
import seaborn as sns
import pandas as pd

import matplotlib.animation as animation
import numpy as np
from pylab import *


def update_img(n):
    print n
    sns.heatmap(dframe[n*100000:(n+1)*100000].corr(), annot=False, fmt="2.2f", cmap="afmhot_r", vmin=0, vmax=1, cbar=False)


if __name__ == '__main__':
    window = 400
    lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                    'e140220']

    # Good experiments
    lexperiments = ['e130827',  'e141016', 'e140911', 'e140225', 'e140220']

    # lexperiments = ['e140225', 'e140220', 'e141016', 'e140911']
    lexperiments = ['e140515']

    TVD = False
    ext = ''
    peakdata = {}
    for expname in lexperiments:
        if TVD:
            alt = 'TVD'
        else:
            alt = ''

        datainfo = experiments[expname]
        f = h5py.File(datainfo.dpath + datainfo.name + ext + '.hdf5', 'r+')

        # fig = plt.figure()
        dpi = 200

        fig, ax = plt.subplots(figsize=(10, 10))
        for dfile in datainfo.datafiles:
            d = np.array(f[dfile + '/' + 'Raw'])
            dframe = pd.DataFrame(d, columns=datainfo.sensors)

            ani = animation.FuncAnimation(fig, update_img, 60, interval=30)
            writer = animation.writers['ffmpeg'](fps=1)

            ani.save(datainfo.dpath+'/Results/'+dfile+'correl.mp4',writer=writer,dpi=dpi)

