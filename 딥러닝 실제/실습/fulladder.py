#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
딥러닝 실제

전가산기(Full Adder)를 구현하는 파이썬 프로그램을 구현
학번 : 2024254022
이름 : 정현일

@author: chohi

Created on Thu Mar 21 13:43:31 2024
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


def FullAdder(x1, x2, x3):
    s1 = XOR(x1, x2)
    s2 = XOR(s1, x3)
    t1 = AND(s1, x3)
    t2 = AND(x1, x2)
    c1 = OR(t1, t2)
    
    return s2, c1


print('FullAdder')
print(FullAdder(0,0,0))
print(FullAdder(0,0,1))

print(FullAdder(1,0,0))
print(FullAdder(1,0,1))

print(FullAdder(0,1,0))
print(FullAdder(0,1,1))

print(FullAdder(1,1,0))
print(FullAdder(1,1,1))   



    
