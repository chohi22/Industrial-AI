#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 21:16:43 2024

@author: chohi
"""

import matplotlib.pyplot as plt
from matplotlib.image import imread

img = imread('/Users/chohi/Desktop/chohi.png')

plt.imshow(img)
plt.show()
