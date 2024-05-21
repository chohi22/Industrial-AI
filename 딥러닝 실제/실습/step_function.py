#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 19:01:56 2024

@author: chohi
"""

import numpy as np
import matplotlib.pylab as plt

def step_function(x):
    return np.array(x > 0, dtype = np.int)


x = np.arange(-5.0, 5.0, 0.1)

y = step_function(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()

