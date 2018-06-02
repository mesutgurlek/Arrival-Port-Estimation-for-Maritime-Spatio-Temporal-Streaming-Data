#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 22:30:57 2018

@author: melih
"""

from Pagerank import learn, predict

if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Usage: python run.py <filename> <portsfile>")
        sys.exit(1)
    # training_filename = sys.argv[1]
    # ports_filename = sys.argv[2]'''
    training_filename = '../Dataset/preprocess_outputs/transactional_dataset.csv'
    ports_filename = '../Dataset/ports.csv'
    learner = learn.Learner(training_filename, ports_filename)
    predictor = predict.Predictor(learner)
    
    # predict destination port for each port in ports set
    test_ports = [learner.data.loc[i]['DEPARTURE_PORT_NAME'] for i in learner.trip_idxs]
    test_targets = [learner.data.loc[i]['ARRIVAL_PORT_CALC'] for i in learner.trip_idxs]
    acc, preds = predictor.predict(test_ports, test_targets)
    # print(preds[:10])
    print(acc)

#training_filename = '/home/melih/Desktop/METU/2.Donem/Ceng514_DataMining/514_Project/Dataset/training_dataset.csv'
#ports_filename = '/home/melih/Desktop/METU/2.Donem/Ceng514_DataMining/514_Project/Dataset/ports.csv'
