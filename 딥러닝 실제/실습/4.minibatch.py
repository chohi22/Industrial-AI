#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 20:08:01 2024

@author: chohi
"""

import sys, os
sys.path.append(os.pardir)
import numpy as np
from mnist import load_mnist


(x_train, t_train), (x_test, y_test) = load_mnist(normalize=True, one_hot_label=True)


print(x_train.shape)
print(t_train.shape)


train_size = x_train.shape[0]
batch_size = 10
batch_mask = np.random.choice(train_size, batch_size)
x = batch = x_train[batch_mask]
y = batch = t_train[batch_mask]

print(x)
print(y)