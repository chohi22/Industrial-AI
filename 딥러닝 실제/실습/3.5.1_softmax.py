#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 19:36:44 2024

@author: chohi
"""

import numpy as np


def softmax(a):
    exp_a = np.exp(a)
    sum_sum_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    
    return y


a = np.array([0.3, 2.9, 4.0])

exp_a = np.exp(a)
print(exp_a)


sum_exp_a = np.sum(exp_a)
print(sum_exp_a)


y = exp_a / sum_exp_a
print(y)

print(softmax(a))
