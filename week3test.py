# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:02:00 2019

@author: reem_
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math 
from matplotlib import cm



def plotResults(sample_means, intervals):    
    threshold = 40000
    x = np.arange(4)
   
    fig, ax = plt.subplots()
    cmap = plt.cm.RdBu
    top = [threshold - x for x in sample_means]
    norm = mcolors.Normalize(vmin=-10000, vmax=10000)
    ax.bar(x, sample_means, width =0.8, color=cmap(norm(top)))
    ax.set_xticks(x, ('1992','1993','1994','1995'))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm)
   
    plt.errorbar(x=['1992','1993','1994','1995'], 
                 y=sample_means, 
             yerr=[(top-bot)/2 for top,bot in intervals],
             fmt='o', ecolor ='k')
    
    plt.hlines(y=threshold, xmin= x.argmin()-0.8,xmax=x.argmax()+0.8, colors='g', label = threshold)


    plt.show()
    fig.savefig('week3.png')

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                   index=[1992,1993,1994,1995])

sample_size = 1500

intervals = []
sample_means = []


    
for i  in range(0,4):
    pop = df.iloc[i,:]
    sample = np.random.choice(a= pop, size = sample_size)
    sample_mean = round(sample.mean())
    sample_means.append(sample_mean)

    z_critical = stats.norm.ppf(q = 0.95)  # Get the z-critical value*         

    pop_stdev = pop.std()  # Get the population standard deviation

    stats.norm.ppf(q = 0.025)

    margin_of_error = z_critical * (pop_stdev/math.sqrt(sample_size))

    confidence_interval = (sample_mean - margin_of_error,
                           sample_mean + margin_of_error)  
    
    intervals.append(confidence_interval)
    
print(intervals)
print(sample_means)

plotResults(sample_means, intervals)



