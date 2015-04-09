"""
.. module:: ClustersCompare

ClustersCompare
*************

:Description: ClustersCompare

    

:Authors: bejar
    

:Version: 

:Created on: 20/01/2015 7:29 

"""

__author__ = 'bejar'

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

nc = 16
alg1 = 'spectral'
alg2 = 'kmeans'

# for line, _, _ in aline:
# print 'LINE=', line
#
#     matclust1 = scipy.io.loadmat(clustpath + 'cluster-'+alg1+'-peaks-' + line + '-nc' + str(nc) + '.mat')
#     matclust2 = scipy.io.loadmat(clustpath + 'cluster-'+alg2+'-peaks-' + line + '-nc' + str(nc) + '.mat')
#
#     centers1 = matclust1['centers']
#     print centers1.shape
#     centers2 = matclust2['centers']
#     print centers2.shape
#
#     dist = euclidean_distances(centers1, centers2)
#
#     m = Munkres()
#     indexes = m.compute(dist.copy())
#     sumdist = 0
#
#     for c1, c2 in indexes:
#         sumdist += euclidean_distances(centers1[c1], centers2[c2])
#     print sumdist
#
#     #print indexes

# for line, _, _ in aline:
#     print 'LINE=', line
#
#     matclust1 = scipy.io.loadmat(clusterpath + 'cluster-'+alg1+'-peaks-' + line + '-nc' + str(nc) + '.mat')
#     matclust2 = scipy.io.loadmat(clusterpath + 'cluster-'+alg2+'-peaks-' + line + '-nc' + str(nc) + '.mat')
#
#     labels1 = matclust1['labels'][0]
#     # print labels1.shape
#     labels2 = matclust2['labels'][0]
#     # print labels2.shape
#
#
#     print 'NMI= ', normalized_mutual_info_score(labels1, labels2)
#     print 'ARAND= ', adjusted_rand_score(labels1, labels2)
#     print 'AMI= ', adjusted_mutual_info_score(labels1, labels2)

# lcenters = []
# for line, _, _ in aline:
#     #print 'LINE=', line
#
#     matclust1 = scipy.io.loadmat(clusterpath + 'cluster-'+alg1+'-peaks-' + line + '-nc' + str(nc) + '.mat')
#     centers1 = matclust1['centers']
#     lcenters.append(centers1)
#
#
# mdist = np.zeros((len(lcenters), len(lcenters)))
# for i in range(len(lcenters)):
#     for j in range(len(lcenters)):
#         dist = euclidean_distances(lcenters[i], lcenters[j])
#         m = Munkres()
#         indexes = m.compute(dist.copy())
#
#         sumdist = 0
#         for c1, c2 in indexes:
#             sumdist += euclidean_distances(lcenters[i][c1], lcenters[j][c2])
#         mdist[i, j] = sumdist
#         print aline[i][0], aline[j][0], sumdist
#     print '---------------------'
