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
from operator import itemgetter



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

        d = np.array(f[datainfo.datafiles[0] + '/' + 'Raw'])
        corrmat = np.corrcoef(d, rowvar=0)
        ylabels = []
        for i, si in enumerate(datainfo.sensors):
            for j, sj in enumerate(datainfo.sensors):
                if i < j:
                    ylabels.append((si+'-'+sj, corrmat[i,j]))

        ylabels = sorted(ylabels, key=itemgetter(1))
        ylabels = [x for x,_ in ylabels]
        for dfile in datainfo.datafiles:
            print dfile
            d = np.array(f[dfile + '/' + 'Raw'])
            corrmat = np.corrcoef(d, rowvar=0)
            fig, ax = plt.subplots(figsize=(20, 20))

            # print dframe.corr()
            # print corrmat
            # sns.corrplot(dframe,  cmap="afmhot_r", sig_stars=False, cmap_range=(0, 1))
            # sns.heatmap(dframe.corr(), annot=True, fmt="2.2f", cmap="afmhot_r")
            #
            # plt.title(dfile, fontsize=48)
            # plt.savefig(datainfo.dpath + '/Results/' + dfile + '-corr2.pdf', orientation='landscape', format='pdf')
            # plt.close()
            # np.savetxt(datainfo.dpath + '/Results/' + dfile + '-corr.csv', corrmat, fmt='%.8e', delimiter=',', newline='\n')


            dlabels = {}
            for i, si in enumerate(datainfo.sensors):
                for j, sj in enumerate(datainfo.sensors):
                    if i < j:
                        dlabels[si+'-'+sj] = corrmat[i,j]

            ydata = [dlabels[x] for x in ylabels]
            #fig = plt.figure()
            plt.barh(range(len(ylabels)), ydata, align='center', alpha=0.4)
            plt.yticks(range(len(ylabels)), ylabels)
            plt.xlabel('Correlation')
            plt.title(dfile)


            #cg = sns.clustermap(dframe.corr(), standard_scale=True, cmap="afmhot_r", method="average")
            #plt.title(dfile, fontsize=48)
            plt.savefig(datainfo.dpath + '/Results/' + dfile + '-histo.pdf', orientation='landscape', format='pdf')
            #plt.show()
            plt.close()
