#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:21:09 2024

@author: chohi
"""

import numpy as np
import matplotlib.pylab as plt


def sigmod(x):
    return 1 / (1 + np.exp(-x))



x = np.arange(-5.0, 5.0,0.1)


y2 = sigmod(x)
plt.plot(x, y2)
plt.ylim(-0.1, 1.1)
plt.show()

