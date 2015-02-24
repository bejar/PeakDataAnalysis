"""
.. module:: ClusterNumberPeaks

ClusterNumberPeaks
*************

:Description: ClusterNumberPeaks

    

:Authors: bejar
    

:Version: 

:Created on: 21/01/2015 13:45 

"""

__author__ = 'bejar'

from kemlglearn.metrics import scatter_matrices_scores, davies_bouldin_score
import scipy.io
import numpy as np
from config.paths import clusterpath, datapath
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation, DBSCAN, SpectralClustering
from collections import Counter
from util.plots import plotSignals

def normalize(data):
    """
    Normalizes all peaks to N(0,1)

    :param data:
    :return:
    """
    ndata = np.zeros(data.shape)

    for i in range(data.shape[0]):
        mean = np.mean(data[i])
        std = np.std(data[i])
        ndata[i] += (data[i]-mean)/std

    return ndata


aline = [
        ('L4cd', 'k9.n5', 9),
        ('L4ci', 'k9.n1', 9),
        ('L5cd', 'k10.n6', 10),
        ('L5rd', 'k20.n1', 10),
        ('L5ci', 'k15.n1', 15),
        ('L5ri', 'k15.n9', 15),
        ('L6cd', 'k17.n1', 17),
        ('L6rd', 'k13.n9', 13),
        ('L6ci', 'k15.n1', 10),
        ('L6ri', 'k18.n4', 18),
        ('L7ri', 'k18.n4', 18)
        ]
alg = 'kmeans'

for line, _, _ in aline:
    print 'LINE=', line
#    print cpath + '/WHOLE/trazos.' + line + '.mat'
    matpeaks = scipy.io.loadmat(datapath + '/WHOLE/trazos.' + line + '.mat')
#    print matpeaks['Trazos'].shape
    data = matpeaks['Trazos']
    data = normalize(data)

    # minc = {'ZCF': np.inf, 'DB': np.inf}
    # chosen = {'ZCF': -1, 'DB': -1}
    minc = {'DB': np.inf, 'ZCF': np.inf, 'CH': np.inf}
    chosen = {'DB': -1}
    for nc in range(2, 16):
        score = {'DB':  np.inf, 'ZCF': 0, 'CH': 0}
        for rep in range(5):
            if alg == 'kmeans':
                cluster = KMeans(n_clusters=nc, n_jobs=-1)
            elif cluster == 'spectral':
                cluster = SpectralClustering(n_clusters=nc, assign_labels='discretize',
                                             affinity='nearest_neighbors', n_neighbors=30)


            cluster.fit(data)
            #score = scatter_matrices_scores(data, cluster.labels_, ['ZCF'])
            minscore = davies_bouldin_score(data, cluster.labels_)
            if score['DB'] > minscore:
                score['DB'] = minscore
                # oscores = scatter_matrices_scores(data, cluster.labels_, ['ZCF', 'CH'])
                # for sc in oscores:
                #     score[sc] = oscores[sc]
                print '.',
        for sc in score:
            if minc[sc] > score[sc]:
                minc[sc] = score[sc]
                chosen[sc] = nc
        print nc, score

    print chosen
    nc = chosen['DB']

    km = KMeans(n_clusters=nc, n_jobs=-1)
    km.fit(data)
    lab = km.labels_
    centers = np.zeros((nc, data.shape[1]))

    for i in range(data.shape[0]):
        centers[lab[i]] += data[i]
    print len(lab)
    l = [lab[i] for i in range(len(lab))]
    c = Counter(l)
    print c

    # Save the results
    lcenters = []
    numex = np.zeros(nc)
    for i in c:
        centers[i] /= c[i]
        print i, c[i]
        numex[i] = c[i]
        lcenters.append((centers[i], 'center %d' % i))

    cstd = np.zeros((nc, data.shape[1]))
    for i in c:
        center_mask = lab == i
        cstd[i] = np.std(data[center_mask], axis=0)


    mx = np.max(centers) # 0.26
    mn = np.min(centers) #-0.06

    plotSignals(lcenters, 8, 2, mx, mn, 'cluster-'+alg+'-N-%s-NC%d' % (line, nc), 'cluster-'+alg+'-%sNC%d' % (line, nc), clusterpath, cstd=cstd)

    #
    # if alg == 'spectral':
    #     params = {'clalg': 'spectral',
    #                        'nc': nc,
    #                        'labels': 'discretize',
    #                        'affinity': 'nearest_neighbors',
    #                        'n_neigbors': 30
    #                        }
    # elif alg == 'kmeans':
    #     params = {'clalg': 'kmeans', 'nc': nc}
    # peakdata = {'labels': lab,
    #             'centers': centers,
    #             'numex': numex,
    #             'params': params
    #             }
    #
    # scipy.io.savemat(clusterpath + 'cluster-'+alg+'-peaks-N' + line + '-nc' + str(nc) + '.mat', peakdata)