"""
.. module:: experiments

experiments
*************

:Description: experiments

    Experiment objects

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 11:44 

"""

__author__ = 'bejar'

from util.Experiment import Experiment
from config.paths import cinvesdata

datafiles = [(['e130716f00-cntrl1', 'e130716f02-cntrl2', 'e130716f03-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e130827f23-cntrl1', 'e130827f26-cntrl2', 'e130827f37-cntrl3'], 11,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri'],
              10256.4),
             (['e130903f20-cntrl1', 'e130903f22-cntrl2', 'e130903f25-cntrl3'], 11,
              ['L4ri', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci'],
              10256.4),
             (['e141113f09-cntrl1', 'e141113f11-cntrl2', 'e141113f13-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e141029f35-cntrl1', 'e141029f37-cntrl2', 'e141029f39-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e141016f07-cntrl1', 'e141016f09-cntrl2', 'e141016f11-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e140911f20-cntrl1', 'e140911f33-cntrl2', 'e140911f36-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10416.7),
             (['e140311f09-cntrl1', 'e140311f13-cntrl2', 'e140311f23-cntrl3'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e140225f31-cntrl1', 'e140225f34-cntrl2', 'e140225f39-cntrl3', 'e140225f47-cntrl4', 'e140225f50-cntrl5',
               'e140225f59-cntrl6'], 12,
              ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
              10204.1),
             (['e140220f8-ctrl1', 'e140220f10-ctrl2', 'e140220f12-ctrl3'], 12,
              ['DRP', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci', 'L7ri'],
              10416.7),
             ]

lexperiments = ['e130716', 'e130827', 'e130903', 'e141113', 'e141029', 'e141016', 'e140911', 'e140311', 'e140225',
                'e140220']

experiments = \
    {
        'e140515':
             Experiment(cinvesdata, 'e140515', 10000.0,
                       ['15514005', '15514006', '15514007',
                        '15514008', '15514009', '15514010', '15514011', '15514012', '15514013', '15514014', '15514015', '15514016',
                        '15514017', '15514018', '15514019', '15514020', '15514021', '15514022', '15514023', '15514024', '15514025', '15514026', '15514027'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
                        []),
        'e140515b':
             Experiment(cinvesdata, 'e140515', 10000.0,
                       ['15514005', '15514006', '15514007',
                        '15514008', '15514009', '15514010', '15514011', '15514012', '15514013', '15514014', '15514015', '15514016',
                        '15514017', '15514018', '15514019', '15514020', '15514021'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
                        [8,8,8,8,8,8,8,8,8,8,8,8]),

        'e130716':
            Experiment(cinvesdata, 'e130716', 10204.1,
                       ['e130716f00-cntrl1', 'e130716f02-cntrl2', 'e130716f03-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'],[8,8,8,8,8,8,8,8,8,8,8,8]),
        'e130827':
            Experiment(cinvesdata, 'e130827', 10256.4,
                       ['e130827f23-cntrl1', 'e130827f26-cntrl2', 'e130827f37-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri']
                       , [12, 10, 12, 10, 12, 11, 11, 14, 13, 11, 11]),#[9, 10, 11, 9, 11, 11, 11, 10, 8, 12, 8]
        'e130903':
            Experiment(cinvesdata, 'e130903', 10256.4,
                       ['e130903f20-cntrl1', 'e130903f22-cntrl2', 'e130903f25-cntrl3'],
                       ['L4ri', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci'],[]),
        'e141113':
            Experiment(cinvesdata, 'e141113', 10204.1,
                       ['e141029f35-cntrl1', 'e141029f37-cntrl2', 'e141029f39-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'],[8,8,8,8,8,8,8,8,8,8,8,8]),

        'e141029':
            Experiment(cinvesdata, 'e141029', 10204.1,
                       ['e141029f35-cntrl1', 'e141029f37-cntrl2', 'e141029f39-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'],[8,8,8,8,8,8,8,8,8,8,8,8]),
        'e141016':
            Experiment(cinvesdata, 'e141016', 10204.1,
                       ['e141016f07-cntrl1', 'e141016f09-cntrl2', 'e141016f11-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'],[9, 8, 10, 8, 8, 8, 9, 10, 7, 7, 10, 8]),
        'e140911':
            Experiment(cinvesdata, 'e140911', 10416.7,
                       ['e140911f20-cntrl1', 'e140911f33-cntrl2', 'e140911f36-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'], [6, 6, 7, 7, 7, 7, 7, 8, 6, 6, 6, 8]),
        'e140311':
            Experiment(cinvesdata, 'e140311', 10204.1,
                       ['e140311f09-cntrl1', 'e140311f13-cntrl2', 'e140311f23-cntrl3'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'],[8,8,8,8,8,8,8,8,8,8,8,8]),
        'e140225':
            Experiment(cinvesdata, 'e140225', 10204.1,
                       ['e140225f31-cntrl1', 'e140225f34-cntrl2', 'e140225f39-cntrl3', 'e140225f47-cntrl4',
                        'e140225f50-cntrl5', 'e140225f59-cntrl6'],
                       ['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri',
                        'L7rd'], [8, 7, 7, 7, 7, 8, 8, 7, 8, 8, 6, 6]), #[13, 12, 16, 14, 14, 13, 13, 13, 14, 10, 10, 12]
        'e140220':
            Experiment(cinvesdata, 'e140220', 10416.7,
                       ['e140220f8-ctrl1', 'e140220f10-ctrl2', 'e140220f12-ctrl3'],
                       ['DRP', 'L4cd', 'L4ci', 'L5rd', 'L5ri', 'L5cd', 'L5ci', 'L6rd', 'L6ri', 'L6cd', 'L6ci', 'L7ri'],
               [10, 8, 10, 9, 9, 8, 8, 8, 10, 9, 6, 10])
    }