#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:38:12 2024

@author: chohi
"""


import numpy as np


a = np.array([[1,2,3], [4,5,6]])
print(a.shape)

b = np.array([[1,2], [3,4], [5,6]])
print(b.shape)

print(np.dot(a,b))

c = np.array([[1,2], [3,4]])
print(c.shape)

print(np.dot(a,c))