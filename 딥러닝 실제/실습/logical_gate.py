#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:47:12 2024

@author: chohi
"""

import numpy as np


def NAND (x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1
    
    
def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    
    tmp = np.sum(w*x) + b
    
    if tmp <= 0:
        return 0
    else:
        return 1 
    
    
    
def AND (x1, x2):
    x = np.array([x1,x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1
    

def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y    


def HalfAdd(x1, x2):
    s1 = XOR(x1, x2)
    c = AND(x1, x2)
    return c, s1 
    

print('AND')
print(AND(0,0))
print(AND(1,0))
print(AND(0,1))
print(AND(1,1))


print('NAND')

print(NAND(0,0))
print(NAND(1,0))
print(NAND(0,1))
print(NAND(1,1))


print('OR')
print(OR(0,0))
print(OR(1,0))
print(OR(0,1))
print(OR(1,1))

print('XOR')
print(XOR(0,0))
print(XOR(1,0))
print(XOR(0,1))
print(XOR(1,1))

print('HalfAdd')
print(HalfAdd(0,0))
print(HalfAdd(1,0))
print(HalfAdd(0,1))
print(HalfAdd(1,1))