#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:46:50 2024

@author: chohi
"""

import numpy as np

def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    
    return y



a = np.array([0.3, 2.9, 4.0])
y = softmax(a)

print(y)

print(np.sum(y))
