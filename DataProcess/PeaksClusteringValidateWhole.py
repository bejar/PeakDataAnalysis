"""
.. module:: PeaksClusteringValidate

PeaksClusteringValidate
*************

:Description: PeaksClusteringValidate

 Explores the possible number of clusters for the signals of using all the data of the phases of the experiments
using AMI stability


:Authors: bejar
    

:Version: 

:Created on: 06/05/2015 12:10 

"""

__author__ = 'bejar'


from numpy import mean, std
from sklearn import metrics
import h5py
import numpy as np
from sklearn.cluster import KMeans

from config.experiments import experiments
from util.plots import show_signal, plotSignals
from collections import Counter
import logging


lexperiments = ['e130827',  'e141016', 'e140911', 'e140225','e140220']


expname = 'e140911'
niter = 30
datainfo = experiments[expname]

logging.basicConfig(filename=datainfo.dpath+'/Results/' + datainfo.name + '-val-whole.txt', filemode='w',
                    level=logging.INFO, format='%(message)s', datefmt='%m/%d/%Y %I:%M:%S')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

f = h5py.File(datainfo.dpath + datainfo.name + '.hdf5', 'r+')

logging.info('****************************')
for s in datainfo.sensors:
    ldata = []
    for dfiles in datainfo.datafiles:
        d = f[dfiles + '/' + s + '/' + 'PeaksResamplePCA']
        dataf = d[()]
        ldata.append(dataf)

    data = np.concatenate(ldata)
    best = 0
    ncbest = 0
    logging.info('S= %s' %s)
    for nc in range(4, 21):
        lclasif = []
        for i in range(niter):
            k_means = KMeans(init='k-means++', n_clusters=nc, n_init=10, n_jobs=-1)
            k_means.fit(data)
            lclasif.append(k_means.labels_.copy())
            print '.',
        vnmi = []
        for i in range(niter):
            for j in range(i+1, niter):
                nmi=metrics.adjusted_mutual_info_score(lclasif[i], lclasif[j])
                vnmi.append(nmi)
        mn = mean(vnmi)
        if best < mn:
            best = mn
            ncbest = nc
        #print nc, mn
        logging.info('%d  %f' % (nc, mn))

    logging.info('S= %s NC= %d' % (s, ncbest))
    logging.info('****************************')