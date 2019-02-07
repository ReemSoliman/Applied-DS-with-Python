# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 12:14:13 2019

@author: reem_
"""

import pandas as pd
import numpy as np
import re


def check_country_name(x):
    p = re.compile(r'[\(\d]')
    m=  p.split(x)[0].strip()
    return m

def check_renwable(x, med):
    if x>= med:
        return 1
    else:
        return 0

##########
##Prepare Data
def question_1():
    energy= pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols="C:F" )
    energy.columns =['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy['Energy Supply'].replace('...', np.NaN, inplace=True)
    energy['Energy Supply per Capita'].replace('...', np.NaN, inplace=True)
    energy['Energy Supply'] *= 1000000#.apply(lambda x: x/1000000 )
    energy['Country'].replace('Republic of Korea', 'South Korea', inplace=True)
    energy['Country'].replace('United States of America20', 'United States', inplace=True)
    energy['Country'].replace('United Kingdom of Great Britain and Northern Ireland19', 'United Kingdom', inplace=True)
    energy['Country'].replace('China, Hong Kong Special Administrative Region3', 'Hong Kong', inplace=True)
    energy['Country'] = energy['Country'].apply(check_country_name)
    
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP['Country Name'].replace('Korea, Rep.', 'South Korea', inplace=True)
    GDP['Country Name'].replace('Iran, Islamic Rep.', 'Iran', inplace=True)
    GDP['Country Name'].replace('Hong Kong SAR, China', 'Hong Kong', inplace=True)
    
    ScimEn= pd.read_excel('scimagojr.xlsx')
    
    ##Q1
    GDP1 = GDP.iloc[:,  -14:-4]
    GDP1['Country']= GDP['Country Name']
    
    ScimEn_top15 = ScimEn.iloc[0:15]
    
    Top15 = ScimEn_top15.merge(energy, how='inner',  left_on='Country', right_on='Country').merge(GDP1, how='inner',  left_on='Country', right_on='Country')
    Top15.set_index ("Country", inplace=True)
    return Top15

    ##Q2
def question_2():
    Top15 = question_1()
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    return str(len(GDP)-len(Top15))
##Q3
#from
def question_3(): 
    Top15 = question_1()
    def avgGDP(row):
        data = row[-10:]
        return pd.Series({'avgGDP': data.mean()}) 
    avgGDP_series = Top15.apply(avgGDP, axis = 1).sort_values(by = "avgGDP",
                    ascending = False)['avgGDP']
    return avgGDP_series

#GDP = pd.read_csv('world_bank.csv', skiprows=4)
#    GDP1 = GDP.iloc[:,  -12:-2]
#    GDP1['Country']= GDP['Country Name']
#q3 = Top15['Country'].to_frame().merge(GDP1, how='inner',  left_on='Country', right_on='Country')
#q3.set_index("Country", inplace=True)
#q3s = q3.apply(func=np.mean, axis=1).sort_values(ascending= False)
##Q4
#GDP1.loc[GDP1['Country'] == q3s.keys()[5]]['2017'] - GDP1.loc[GDP1['Country'] == q3s.keys()[5]]['2008']
def question_4():
    Top15 = question_1()
    avgGDP = question_3()
    idx = avgGDP.index[5]
    return Top15.loc[idx]['2015'] - Top15.loc[idx]['2006']
##Q6
def question_5():
    Top15 = question_1()
    return Top15["Energy Supply per Capita"].mean()
def question_6():
    Top15 = question_1()
    return Top15["% Renewable"].idxmax(), Top15["% Renewable"].max()
##Q7
def question_7():
    Top15 = question_1()
    Top15['Citation_Ratio'] = Top15['Self-citations']/ Top15['Citations']
    return Top15.Citation_Ratio.idxmax(), Top15.Citation_Ratio.max()
##Q8
def question_8():
    Top15 = question_1()
    Top15['PopEst'] = Top15['Energy Supply']/ Top15['Energy Supply per Capita']
    Top15.sort_values('PopEst',inplace = True, ascending= False )    
    return Top15.index[2]

def question_9():
    Top15 = question_1()
    Top15['PopEst'] = Top15['Energy Supply']/ Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents']/Top15['PopEst']
    c = Top15[["Citable docs per Capita","Energy Supply per Capita"]].corr()
    return c.iloc[0,1]
def plot9():
    import matplotlib as plt
    Top15 = question_1()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

def question_10():
    Top15 = question_1()    
    m = Top15['% Renewable'].median()
    Top15.sort_values(by = 'Rank',inplace = True)     
    Top15['above_Renwable_med'] = (Top15['% Renewable']>= m).astype(int)
    HighRenew = Top15.loc[Top15['above_Renwable_med'] == 1]['% Renewable']
    return HighRenew

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def question_11():
    Top15 = question_1()
    Top15['PopEst'] = Top15['Energy Supply']/ Top15['Energy Supply per Capita']
    cm = Top15.groupby(by=ContinentDict)['PopEst'].agg([np.size, np.sum, np.mean,np.std])
    return cm
def question_12():
    Top15 = question_1()
    n= pd.cut(Top15['% Renewable'],bins=5)
    return pd.Series(Top15.groupby(by=[ContinentDict,n] ).size())  
def question_13():
    Top15 = question_1()
    Top15['PopEst'] = Top15['Energy Supply']/ Top15['Energy Supply per Capita']
    popEst = Top15['PopEst'] 
    return popEst.apply(lambda x: "{:,}".format(x))

print("###Q1###")
print(question_1())
print("###Q2###")
print(question_2())
print("###Q3###")
print(question_3())
print("###Q4###")
print(question_4())
print("###Q5###")
print(question_5())     
print("###Q6###")
print(question_6())
print("###Q7###")
print(question_7())
print("###Q8###")
print(question_8())
print("###Q9###")
print(question_9())
#print(plot9())
print("###Q10###")
print(question_10())
print("###Q11###")
print(question_11())
print("###Q12###")
print(question_12())
print("###Q13###")
print(question_13())