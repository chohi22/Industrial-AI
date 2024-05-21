#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:35:22 2024

@author: chohi
"""


import numpy as np


a = np.array([[1,2], [3,4]])
print(a.shape)

b = np.array([[5,6], [7,8]])
print(b.shape)

print(np.dot(a,b))

