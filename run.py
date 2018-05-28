#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 22:30:57 2018

@author: melih
"""

import sys
import learn
    


    
if __name__ == "__main__":
    '''if len(sys.argv) != 3:
        print("Usage: python run.py <filename> <portsfile>")
        sys.exit(1)
    # training_filename = sys.argv[1]
    # ports_filename = sys.argv[2]'''
    training_filename = '../Dataset/training_dataset.csv'
    ports_filename = '../Dataset/ports.csv'
    learn.Learner(training_filename, ports_filename)

#training_filename = '/home/melih/Desktop/METU/2.Donem/Ceng514_DataMining/514_Project/Dataset/training_dataset.csv'
#ports_filename = '/home/melih/Desktop/METU/2.Donem/Ceng514_DataMining/514_Project/Dataset/ports.csv'
