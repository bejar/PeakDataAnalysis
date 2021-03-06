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
from Config.paths import datapath

__author__ = 'bejar'

# Lista de conveniencia para poder procesar varios experimentos a la vez
lexperiments = ['e150514']

# Diccionario con los datos de cada experimento
# Todos los experimentos estan en el directorio cinvesdata dentro de una carpeta que tenga el nombre del experimento
experiments = \
    {
        'e150707':
            Experiment(
                dpath='/home/bejar/storage/Data/Gatos/',
                name='e150707',
                sampling=10000.0,
                datafiles=['15707000', '15707001', '15707002', '15707003', '15707004', '15707005', '15707006', '15707007',
                           '15707008', '15707009', '15707010', '15707011', '15707012', '15707013', '15707014', '15707015',
                           '15707016', '15707017', '15707018', '15707019', '15707020', '15707021', '15707022', '15707023',
                           '15707024', '15707025', '15707026', '15707027', '15707028', '15707029', '15707030', '15707031',
                           '15707032', '15707035', '15707036', '15708000', '15708001', '15708002', '15708003', '15708004',
                           '15708005', '15708006', '15708007', '15708008'],
                sensors=['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
                abfsensors=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                clusters=[12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                colors='bbbbyyyyyyyyyyrrrrrrrrryyyyyyyyyyygggyyyyyyy',
                peaks_id_params={'wtime': 120e-3, 'low': 0, 'high': 70, 'threshold': 0.05},
                peaks_resampling={'wtsel': 100, 'rsfactor': 6.0, 'filtered': False},
                peaks_smooth={'pcasmooth': True, 'components': 10, 'wbaseline': 20},
                peaks_filter={'lowpass': 1.0, 'highpass':200.0},
                expnames=['ctrl1', 'ctrl2', 'ctrl3', 'ctrl4', 'lido11', 'lido12', 'lido13', 'lido14', 'lido15', 'lido16',
                          'lido17', 'lido18', 'lido19', 'lido110', 'capsa1', 'capsa2', 'capsa3', 'capsa4', 'capsa5',
                          'capsa6', 'capsa7', 'capsa8', 'capsa9', 'lido21', 'lido22', 'lido23', 'lido24', 'lido25',
                          'lido26', 'lido27', 'lido28', 'lido29', 'lido210', 'esp1', 'esp2', 'esp3', 'lido31', 'lido32',
                          'lido33', 'lido34', 'lido35', 'lido36', 'lido37']

            ),

       'e150514':
            Experiment(
                dpath='/home/bejar/storage/Data/Gatos/',
                name='e150514',
                sampling=10000.0,
                datafiles=['15514005', '15514006', '15514007', '15514008', '15514009', '15514010', '15514011',
                           '15514012', '15514013', '15514014', '15514015', '15514016', '15514017', '15514018',
                           '15514019', '15514020', '15514021', '15514022', '15514023', '15514024', '15514025',
                           '15514026', '15514027', '15514028', '15514029', '15514030', '15514031', '15514032',
                           '15514033', '15514034', '15514035', '15514036', '15514037', '15514038'],
                sensors=['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri', 'L7rd'],
                abfsensors=[0, 1,2,3,4,5,6,7,8,9,10,11],
                clusters=[12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                colors='rrryyyyyyyyybbbbbbbbbbbrrggggggggg',
                peaks_id_params={'wtime': 120e-3, 'low': 0, 'high': 70, 'threshold': 0.05},
                peaks_resampling={'wtsel': 100, 'rsfactor': 6.0, 'filtered': False},
                peaks_smooth={'pcasmooth': True, 'components': 10, 'wbaseline': 20},
                peaks_filter={'lowpass': 1.0, 'highpass':200.0},
                expnames=['15514005ctr1', '15514006ctr2', '15514007ctr3',
                        '15514008cap1', '15514009cap2', '15514010cap3', '15514011cap4', '15514012cap5', '15514013cap6',
                        '15514014cap7', '15514015cap8', '15514016cap9',
                        '15514017lido1', '15514018lido2', '15514019lido3', '15514020lido4', '15514021lido5',
                        '15514022lido6', '15514023lido7', '15514024lido8', '15514025lido8', '15514026lido10', '15514027lido11',
                        '15514028esp1', '15514029esp2', '15514030lido21',
                        '15514031lido22', '15514032lido23', '15514033lido24', '15514034lido25', '15514035lido26',
                        '15514036lido27', '15514037lido28', '15514038lido29']

            ),

        'e120503':
            Experiment(
                dpath='/home/bejar/storage/Data/Gatos/',
                name='e120503',
                sampling=10416.0,
                datafiles=[
                    '12503f02', '12503f03', '12503f24', '12503f25', '12503f36', '12503f37', '12503f48', '12503f49',
                    '12503f61', '12503f62', '12503f73',  '12503f74', '12503f85', '12503f86'],
                sensors=['L4ci', 'L4cd', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri'],
                abfsensors=[1,2,3,4,5,6,7,8,9,10,11],
                clusters=[12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                colors='rryyyybbbggggg',
                peaks_id_params={'wtime': 120e-3, 'low': 0, 'high': 70, 'threshold': 0.05},
                peaks_resampling={'wtsel': 100, 'rsfactor': 6.0, 'filtered': False},
                peaks_smooth={'pcasmooth': True, 'components': 10, 'wbaseline': 20},
                peaks_filter={'lowpass': 1.0, 'highpass':200.0},
                expnames=['ctrl1', 'ctrl2', 'lido11', 'lido12', 'lido13', 'lido14', 'capsa1', 'capsa2', 'capsa3',
                          'lido21', 'lido22', 'lido23', 'lido24', 'lido25']
            ),

        'e110616':
            Experiment(
                dpath='/home/bejar/storage/Data/Gatos/',
                name='e110616',
                sampling=10416.0,
                datafiles=['11616f08', '11616f16', '11616f18',  '11616f29', '11616f30', '11616f31','11616f39', '11616f40',
                           '11616f49', '11616f50', '11616f51', '11616f59', '11617f00', '11617f08', '11617f09'],
                sensors=['L4ci', 'L5ri', 'L5rd', 'L5ci', 'L5cd', 'L6ri', 'L6rd', 'L6ci', 'L6cd', 'L7ri'],
                abfsensors=[1,2,3,4,5,6,7,8,9,10],
                clusters=[12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
                colors='rrryyyyybbbbbbb',
                peaks_id_params={'wtime': 120e-3, 'low': 0, 'high': 70, 'threshold': 0.05},
                peaks_resampling={'wtsel': 100, 'rsfactor': 6.0, 'filtered': False},
                peaks_smooth={'pcasmooth': True, 'components': 10, 'wbaseline': 20},
                peaks_filter={'lowpass': 1.0, 'highpass':200.0},
                expnames=['ctrl1', 'ctrl2', 'ctrl3', 'capsa1', 'capsa2', 'capsa3', 'capsa4', 'capsa5',
                          'lido1', 'lido2', 'lido3', 'lido4', 'lido5', 'lido6', 'lido7']
            ),

    }

if __name__ == '__main__':
    experiment = experiments['e120503']

