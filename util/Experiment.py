"""
.. module:: Experiment

Experiment
*************

:Description: Experiment

    

:Authors: bejar
    

:Version: 

:Created on: 23/03/2015 11:44 

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

    def __init__(self, dpath, name, sampling, datafiles, sensors, clusters, colors, peaks_id_params):
        self.name = name
        self.sampling = sampling
        self.datafiles = datafiles
        self.sensors = sensors
        self.dpath = dpath
        self.clusters = clusters
        self.colors = colors
        self.peaks_id_params = peaks_id_params


