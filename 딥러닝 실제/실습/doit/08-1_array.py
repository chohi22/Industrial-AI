#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:41:03 2024

@author: chohi
"""

import numpy as np
from scipy.signal import convolve
from scipy.signal import correlate


w = np.array([2, 1, 5, 3])
x = np.array([2, 8, 3, 7, 1, 2, 0, 4, 5])


w_r = np.flip(w)
print(w_r)

w_r2 = w[::-1]
print(w_r2)

for i in range(6):
    print(np.dot(x[i:i+4], w_r))
    
    
convolve(x, w, mode='valid')
correlate(x, w, mode='valid')
correlate(x, w, mode='full')
correlate(x, w, mode='same')
         