#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

dataset_path  = 'Dataset/preprocess_outputs/port_calc_processed.csv'

if __name__ == "__main__":

    dataset = read_csv(dataset_path)
    # integer encode direction
    encoder = LabelEncoder()
    dataset = dataset.dropna(axis=0, how='any')
    values = dataset.values
    values[:, 5] = encoder.fit_transform(values[:, 5])
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values[:,[0,1,2,3,4,5]])

    values[:,[0,1,2,3,4,5]] = scaled

    # dividing X, y into train and test data
    X_train, X_test, y_train, y_test = train_test_split(values[:,[0,1,2,3,4,5]], values[:,6], random_state=0)

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train)
    # accuracy on X_test
    accuracyKNN = knn.score(X_test, y_test)
    print(accuracyKNN)
    # -----------------------------------------------------
    from sklearn.svm import SVC
    svm_model_linear = SVC(kernel='linear', C=1).fit(X_train, y_train)
    svm_predictions = svm_model_linear.predict(X_test)
    # model accuracy for X_test
    accuracySVM = svm_model_linear.score(X_test, y_test)
    print(accuracySVM)

    # -----------------------------------------------------

    # training a Naive Bayes classifier
    from sklearn.naive_bayes import GaussianNB

    gnb = GaussianNB().fit(X_train, y_train)
    gnb_predictions = gnb.predict(X_test)

    # accuracy on X_test
    accuracyNB = gnb.score(X_test, y_test)
    print(accuracyNB)