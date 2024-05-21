#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:34:44 2024

@author: chohi
"""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

import matplotlib.pyplot as plt


cancer = load_breast_cancer()
x = cancer.data
y = cancer.target
x_train_all, x_test, y_train_all, y_test = train_test_split(x, y, stratify=y, test_size=0.2, random_state=42)

#
#sgd = SGDClassifier(loss='log', random_state=42)
sgd = SGDClassifier(loss='hinge', random_state=42)
sgd.fit(x_train_all, y_train_all)
sgd.score(x_test, y_test)


# 훈련, 검증, 테스트 세트 6:2:2
x_train, x_val, y_train, y_val = train_test_split(x_train_all, y_train_all, 
                                                  stratify=y_train_all, test_size=0.2, random_state=42)

print(len(x_train), len(x_val))

sgd1 = SGDClassifier(loss='log', random_state=42)
sgd1.fit(x_train, y_train)
sgd1.score(x_val, y_val)

#print(cancer.feature_name[[2,3]])
plt.boxplot(x_train[:,2:4])
plt.xlabel('feature')
plt.ylabel('value')
plt.show()
         