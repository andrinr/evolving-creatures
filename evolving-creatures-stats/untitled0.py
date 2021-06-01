#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 00:42:06 2021

@author: Ronny
"""
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.cm import RdYlBu_r as cMap


fig, axs = plt.subplots(1,4)


mu, sigma = 6, 0.8
s = [[np.random.normal (1, 0.8, 1000)], 
     [np.random.normal (6, 0.8, 1000)],
     [np.random.normal (3.5, 1, 1000)]]

s.append(s[0][:500]+s[1][:500])
fact = 254/(7)
# Create the bins and histogram 
for i in range(3):
    axs[i].set_xlim(1, 6)
    n, bins, patches = axs[i].hist(s[i], bins=7, range=[1, 6], density=True) 

    for i, p in enumerate(patches):
        plt.setp(p, 'facecolor', cMap(round(i * fact)))

n, bins, patches = axs[3].hist(s[3], bins=7, range=[1, 6], density=True) 

for i, p in enumerate(patches):
    plt.setp(p, 'facecolor', cMap(round(i * fact)))

plt.show()