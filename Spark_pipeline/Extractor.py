#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:47:21 2019

@author: ankitachikodi
"""


import pandas as pd
import os
import numpy as np
import re
import sys
from collections import Counter
from scipy.special import expit
from itertools import compress

class FeatureExtractor(object):

    def __init__(self):
        self.idf_vector = None
        self.mean_vector = None
        self.events = None
        self.termWeight = None
        self.normalize = None
        self.flag = None

    def fit_transform(self, sequence, termWeight=None, normalize=None, flag=False, minimum_count=1):
        
        print('====== Transformed train data summary ======')
        self.flag = flag
        self.normalize = normalize
        self.termWeight = termWeight
        
        cntX = []
        for i in range(sequence.shape[0]):
            event_counts = Counter(sequence[i])
            cntX.append(event_counts)
        dfX = pd.DataFrame(cntX)
        dfX = dfX.fillna(0)
        self.events = dfX.columns
        X = dfX.values
        if self.flag:
            flag_vector = np.zeros(X.shape[0])
            if minimum_count > 1:
                dx_i = np.sum(X > 0, axis=0) >= minimum_count
                flag_vector = np.sum(X[:, ~dx_i] > 0, axis=1)
                X = X[:, dx_i]
                self.events = np.array(dfX.columns)[dx_i].tolist()
            X = np.hstack([X, flag_vector.reshape(X.shape[0], 1)])
        
        inst_n, event_n = X.shape
        if self.termWeight == 'tf-idf':
            df_vec = np.sum(X > 0, axis=0)
            self.idf_vector
 = np.log(inst_n / (df_vec + 1e-8))
            idf_matx = X * np.tile(self.idf_vector
, (inst_n, 1)) 
            X = idf_matx
        if self.normalize == 'zero-mean':
            mean_vector = X.mean(axis=0)
            self.mean_vector = mean_vector.reshape(1, event_n)
            X = X - np.tile(self.mean_vector, (inst_n, 1))
        elif self.normalize == 'sigmoid':
            X[X != 0] = expit(X[X != 0])
        X_new = X
        
        print('Train data shape: {}-by-{}\n'.format(X_new.shape[0], X_new.shape[1])) 
        return X_new

    def transform(self, sequence):
        
        print('====== Transformed test data summary ======')
        cntX = []
        for i in range(sequence.shape[0]):
            event_counts = Counter(sequence[i])
            cntX.append(event_counts)
        dfX = pd.DataFrame(cntX)
        dfX = dfX.fillna(0)
        empty_events = set(self.events) - set(dfX.columns)
        for event in empty_events:
            dfX[event] = [0] * len(dfX)
        X = dfX[self.events].values
        if self.flag:
            flag_vector = np.sum(dfX[dfX.columns.difference(self.events)].values > 0, axis=1)
            X = np.hstack([X, flag_vector.reshape(X.shape[0], 1)])
        
        inst_n, event_n = X.shape
        if self.termWeight == 'tf-idf':
            idf_matx = X * np.tile(self.idf_vector
, (inst_n, 1)) 
            X = idf_matx
        if self.normalize == 'zero-mean':
            X = X - np.tile(self.mean_vector, (inst_n, 1))
        elif self.normalize == 'sigmoid':
            X[X != 0] = expit(X[X != 0])
        X_new = X

        print('Test data shape: {}-by-{}\n'.format(X_new.shape[0], X_new.shape[1])) 

        return X_new