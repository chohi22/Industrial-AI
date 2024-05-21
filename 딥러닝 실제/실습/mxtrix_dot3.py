#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:52:47 2024

@author: chohi
"""

import numpy as np


x = np.array([1,2])
print(x.shape)


w = np.array([[1,3,5], [2,4,6]])
print(w)

print(w.shape)

y = np.dot(x, w)
print(y)

