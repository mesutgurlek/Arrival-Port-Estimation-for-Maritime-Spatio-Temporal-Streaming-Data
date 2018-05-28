#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:27:24 2018

@author: Melih Baydar
"""

import pandas as pd
import numpy as np
import math

class Learner():
    
    def __init__(self, training_filename, ports_filename):
        self.data = pd.read_csv(training_filename)
        self.ports = self._read_ports(ports_filename)
        self.trip_idxs = self._extract_trip_start_idxs(self.data.loc[:, 'SHIP_ID'])
        self.prob_mat = None
#        lons = np.array(data.loc[:, 'LON'])
#        lats = np.array(data.loc[:, 'LAT'])
#        deneme = np.array(data.loc[:, 'LON':'LAT'])
#        split_map(deneme)
#        self.world_map = None
    
    def _read_ports(self, filename):
        data = pd.read_csv(filename)
        ports = {}
        for index, port in data.iterrows():
            ports[port['PORT_NAME']] = port['LON':'RADIUS']
        return ports
    
    def _extract_trip_start_idxs(self, ship_ids):
        curr_id = ship_ids[0]
        start_idxs = [0]
        for i, ship_id in enumerate(ship_ids):
            if ship_id != curr_id:
                start_idxs.append(i)
                curr_id = ship_id
        return start_idxs
    
    def is_port(self, lon, lat):
        '''
        Returns name of the current port, returns None if given coordinates
        is not in a port
        '''
        for port_name in self.ports:
            port = self.ports[port_name]
            if pow(port['LON'] - lon, 2) + \
                pow(port['LAT'] - lat, 2) <= pow(port['RADIUS'], 2):
#                return port
                return port_name
        return None
        
    def preprocess(filename):
        print('hi')
        
    def _generate_p2p_pagerank(self, teleport_rate=0.1):
        '''
        Generates port size by port size matrix where each cell is probability
        of going to one port to another
        '''
        port_count = len(self.ports)
        port_mat = np.zeros((port_count, port_count), dtype='f')
        # extract the frequency table for going from each port to other ports
        for idx in self.trip_idxs:
            dep_port_row = self.ports[self.data.loc[idx]['DEPARTURE_PORT_NAME']].name
            arr_port_col = self.ports[self.data.loc[idx]['ARRIVAL_PORT_CALC']].name
            port_mat[dep_port_row][arr_port_col] += 1
        # generate probability matrix of port transitions
        norm_port_mat = port_mat / np.sum(port_mat, axis=1, keepdims=True)
        port_mat = (1 - teleport_rate) * norm_port_mat + teleport_rate / port_count
        # since probability of a ship going to its initial port should be zero,
        # distribute that probability to other ports
        for i in range(port_count):
            port_mat[i] += port_mat[i][i] / (port_count - 1)
            port_mat[i][i] = 0
        pagerank_mat = np.zeros((port_count, port_count), dtype='f')
        print port_mat
        # calculate pagerank probabilities iteratively using power method
        for i in range(port_count):
            print(i)
            prob = np.zeros((1, port_count), dtype='f')
            prob[0][i] = 1
            diff = 100 # total difference between two iterations
            while diff > 1e-5:
                temp = np.sum(prob)
                prob = prob.dot(port_mat)
                diff = abs(np.sum(prob) - temp)
            pagerank_mat[i] = np.copy(prob)
            
        self.prob_mat = pagerank_mat
    
    def split_map(lon_lat, edge=1):
        min_lon = math.floor(min(lon_lat[:, 0]))
        max_lon = math.ceil(max(lon_lat[:, 0]))
        min_lat = math.floor(min(lon_lat[:, 1]))
        max_lat = math.ceil(max(lon_lat[:, 1]))
        dim1 = int(max_lat - min_lat)
        dim2 = int(max_lon - min_lon)
        cells = [[0] * dim2 for i in range(dim1)]
        