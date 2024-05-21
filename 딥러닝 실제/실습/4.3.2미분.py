#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 20:27:40 2024

@author: chohi
"""

import numpy as np
import matplotlib.pyplot as plt

def function_1(x):
    return 0.01 * x ** 2 + 0.1 * x

def numerical_diff(f, x):
    h = 1e-4
    return (f(x+h) - f(x-h)) / (2*h)

x = np.arange(0.0, 20.0, 0.1)
y = function_1(x)

plt.xlabel("x")
plt.ylabel("f(x)")
plt.plot(x, y)
plt.show()

numerical_diff(function_1, 5)

numerical_diff(function_1, 10)
