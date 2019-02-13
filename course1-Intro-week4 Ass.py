# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 12:23:26 2019

@author: reem_
"""
import re
import pandas as pd
import numpy as np

def get_list_of_university_towns():
    university_towns = open("university_towns.txt", "r")
    unitowsList = []
    state =""
    while True:
        line = university_towns.readline()
        if not line: 
            break
        matchedSt = re.match("([A-Z]{1}[a-z]*\s)?([A-Z]{1}[a-z]*\[edit\])",line)
        if matchedSt!= None:
             state = matchedSt.string.split("[")[0]
        else:
            region = line.split("(")[0].strip()
            unitowsList.append([state, region])
        
    university_towns.close()
    return pd.DataFrame(unitowsList, columns=["State", "RegionName"])
print(get_list_of_university_towns())

def get_recession_start():
    gdp= pd.read_excel('gdplev.xls', skiprows=7, usecols="E,G" )
    gdp = gdp.iloc[212:,:]
    gdp.columns=["Quarter","GDP_chained_2009"]
    for i in range(1,len(gdp)-4):
        if gdp.iloc[i].GDP_chained_2009< gdp.iloc[i-1].GDP_chained_2009 and gdp.iloc[i].GDP_chained_2009> gdp.iloc[i+1].GDP_chained_2009 :#and gdp.iloc[i+1].GDP_chained_2009< gdp.iloc[i+2].GDP_chained_2009 and gdp.iloc[i+2].GDP_chained_2009 < gdp.iloc[i+3].GDP_chained_2009:
            return gdp.iloc[i].Quarter
    return None
print(get_recession_start())
#print(get_recession_start())
def get_recession_end():
    gdp= pd.read_excel('gdplev.xls', skiprows=7, usecols="E,G" )
    gdp = gdp.iloc[212:,:]
    gdp.columns=["Quarter","GDP_chained_2009"]
    for i in range(1,len(gdp)-4):
        if gdp.iloc[i].GDP_chained_2009< gdp.iloc[i-1].GDP_chained_2009 and gdp.iloc[i].GDP_chained_2009> gdp.iloc[i+1].GDP_chained_2009 and gdp.iloc[i+1].GDP_chained_2009< gdp.iloc[i+2].GDP_chained_2009 and gdp.iloc[i+2].GDP_chained_2009 < gdp.iloc[i+3].GDP_chained_2009:
            return gdp.iloc[i+3].Quarter#.item()
    return None
print(get_recession_end())
def get_recession_bottom():
     gdp= pd.read_excel('gdplev.xls', skiprows=7, usecols="E,G" )
     gdp = gdp.iloc[212:,:]
     gdp = gdp.reset_index(drop=True)
     gdp.columns=["Quarter","GDP_chained_2009"]
     #print(gdp[(gdp.Quarter == get_recession_start())].GDP_chained_2009)
     idx = pd.to_numeric(gdp.index[(gdp.Quarter == get_recession_start())][0])
     #print(idx)
     '''if gdp.loc[idx].GDP_chained_2009.item() < gdp.loc[idx+1].GDP_chained_2009.item():
         return gdp.loc[idx].Quarter.item()
     else: 
         return gdp.loc[idx+1].Quarter.item()'''
     lastqinrecession = pd.to_numeric(gdp.index[gdp.Quarter == get_recession_end()][0])-2
     #print(lastqinrecession)
     recessionqs = gdp.loc[idx:lastqinrecession]
     idmin = recessionqs.iloc[:,1].idxmin()
     bottomq = recessionqs.loc[idmin].Quarter
     #print(bottomq)
     
     return bottomq
print(get_recession_bottom())

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def convert_housing_data_to_quarters():
    zillow_Housing_prices= pd.read_csv('City_Zhvi_AllHomes.csv' )
    df1 = zillow_Housing_prices.iloc[:, [1,2]]
    #replace state code with state name
    df1 = df1.replace({"State": states})
    df2 = zillow_Housing_prices.iloc[:, 51:251]
    
    quraters = pd.DataFrame()
    quarter = 1
    #split into columns into groups of 3 (3 months)
    dfs = np.split(df2, np.arange(3, len(df2.columns), 3), axis=1)
    for i in range(0,len(dfs)):
        lastMonth = list(dfs[i].columns.values)[-1]
        year = lastMonth.split('-')[0]
        month = int(lastMonth.split('-')[1])
        if month%3 == 0:
            quarter = int(month)/3
        else:
            quarter =3
        colname = year+'q'+str(int(quarter))
        quraters[colname] = dfs[i].agg(func= 'mean', axis=1)
     
    zillow_Housing_prices = pd.concat([df1, quraters], axis=1, sort=False)
    
    return zillow_Housing_prices.set_index(['State', 'RegionName' ])

convert_housing_data_to_quarters()

from scipy import stats
#stats.ttest_ind?
def run_ttest():
    
    zhp = convert_housing_data_to_quarters()
    n = zhp.columns.get_loc(get_recession_start())
    qbefreresstart= zhp.columns[n-1]
    '''rhp = zhp.loc[:, [qbefreresstart, get_recession_bottom()] ]'''
    rhp = zhp.loc[:, [qbefreresstart, get_recession_bottom()] ]
    #print(rhp)'''
    universtytowmshp = get_list_of_university_towns().merge(rhp, how='inner', right_index = True, left_on =['State', 'RegionName'])
    universtytowmshp.set_index(['State', 'RegionName'], inplace =True)
    print(universtytowmshp.head())
    non_universitytownshp = rhp[~rhp.index.isin(universtytowmshp.index)]
    universtytowmshp['ratio'] = universtytowmshp.iloc[:,0]/universtytowmshp.iloc[:,1]
    non_universitytownshp['ratio'] = non_universitytownshp.iloc[:,0]/non_universitytownshp.iloc[:,1]
    universtytowmshp.reset_index(inplace = True)
    non_universitytownshp.reset_index(inplace = True)
    universtytowmshp.dropna(inplace=True)
    non_universitytownshp.dropna(inplace=True)
    #print(non_universitytownshp.head())
    print(universtytowmshp['ratio'] )
    print(non_universitytownshp['ratio'] )
    stats.ttest_ind(universtytowmshp['ratio'], non_universitytownshp['ratio'])
    
    #return x
print(run_ttest())