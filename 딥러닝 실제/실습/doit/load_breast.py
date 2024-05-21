#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:15:00 2024

@author: chohi
"""

from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import numpy as np

cancer = load_breast_cancer()
print(cancer.data.shape, cancer.target.shape)

cancer.data[:3]


plt.boxplot(cancer.data)
plt.xlabel('featuere')
plt.ylabel('value')
plt.show()

cancer.feature_names[[3,13,23]]
np.unique(cancer.target, return_counts=True)

x = cancer.data
y = cancer.target
