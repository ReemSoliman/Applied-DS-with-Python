# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:29:40 2019

@author: reem_
"""

#import plotly.plotly as py  
#import plotly.graph_objs as go  
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly
import plotly.plotly as py
import plotly.figure_factory as ff

import numpy as np
import pandas as pd
import math 
import colorlover as cl

#init_notebook_mode(connected=True)
plotly.tools.set_credentials_file(username='reem_soliman', api_key='pijTCzgE00RnqVDmuGYk')

df_sample = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'Oregon']

values = df_sample_r['TOT_POP'].tolist()
fips = df_sample_r['FIPS'].tolist()

df_sample_r.reset_index(inplace = True)

#diabetes = pd.read_excel("Oregon_diabetes.xlsx", skiprows=3, usecols="C,AW")
#diabetes['ratio']= (diabetes['Number']/df_sample_r['TOT_POP'])
counties = pd.read_csv("Oregon_counties.csv")
counties['Area'] = counties['Area'].apply(lambda x: x.replace(",", ""))
counties['Area'] = counties['Area'].astype(int)
counties['den']= (df_sample_r['TOT_POP']/counties['Area']).apply(lambda x:math.ceil(x))
values = counties['den'].tolist()

endpts = list(np.mgrid[min(values):max(values):9j])


'''colorscale = ["#030512","#1d1d3b","#323268","#3d4b94","#3e6ab0",
              "#4989bc","#60a7c7","#85c5d3","#b7e0e4","#eafcfd"]'''
colorscale = [
    'rgb(193, 193, 193)',
    #'rgb(239,239,239)',
    'rgb(195, 196, 222)',
    'rgb(144,148,194)',
    'rgb(101,104,168)',
    'rgb(65, 53, 132)', "#030512","#1d1d3b","#323268","#3d4b94","#3e6ab0", "#4989bc","#60a7c7", "#85c5d3","#b7e0e4","#eafcfd"
]
#colorscale=cl.scales['7']['seq']['Purples']
#endpts = list(np.linspace(1, 12, len(colorscale) - 1))
              
fig = ff.create_choropleth(
    fips=fips, values=values, scope=['Oregon'], show_state_data=True,
    colorscale=colorscale, binning_endpoints=endpts, round_legend_values=True,
    plot_bgcolor='rgb(229,229,229)',
    paper_bgcolor='rgb(255,255,255)',
    legend_title='Population Per Square Mile by County in Oregon State',
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
    exponent_format=True,
)
py.iplot(fig, filename='oregon_pop_density')