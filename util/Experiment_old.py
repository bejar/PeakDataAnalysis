"""
.. module:: Experiment_old

Experiment_old
*************

:Description: Experiment_old

    

:Authors: bejar
    

:Version: 

:Created on: 03/12/2015 14:37 

"""

__author__ = 'bejar'


class Experiment():
    """
    Class for the experiments
    """
    name = None  # Name of the experiment
    sampling = None # Sampling of the raw signal
    datafiles = None # List with the names of the datafiles
    sensors = None # List with the names of the sensors
    dpath = None # Path of the datafiles
    clusters = None # List with the numer of clusters for each sensor
    colors = '' # Colors to use for histogram of the datafiles peaks
    peaks_id_params = None
    expnames = None

    def __init__(self, dpath, name, sampling, datafiles, sensors, clusters, colors, peaks_id_params, expnames=None):
        self.name = name
        self.sampling = sampling
        self.datafiles = datafiles
        self.sensors = sensors
        self.dpath = dpath
        self.clusters = clusters
        self.colors = colors
        self.peaks_id_params = peaks_id_params
        if expnames is None:
            self.expnames = datafiles
        else:
            self.expnames = expnames
