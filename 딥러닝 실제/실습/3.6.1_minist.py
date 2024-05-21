#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 20:23:45 2024

@author: chohi
"""

import sys, os
sys.path.append(os.pardir)
#from dataset.mnist import load_mnist
from mnist import load_mnist
#from keras.mnist import load_mnist


(x_train, t_train), (x_test, t_test) = load_mnist(flatten = True, normalize=False)

print(x_train.shape)
print(t_train.shape)
print(x_test.shape)
print(t_test.shape)
