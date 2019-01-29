# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 11:09:16 2019

@author: reem_soliman
"""
import pandas as pd
###################################################################
#Part1
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)
#print(df.columns)
names_ids = df.index.str.split('\s\(')
#print(names_ids)

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')

###Q1
#print(df[['Gold']].idxmax().to_string().split(1)) 
print(df.Gold.idxmax())
###Q2
s = abs(df["Gold"] - df["Gold.1"])
df1 = s.to_frame(name='Gold_diff')
print(df1.Gold_diff.idxmax())
#Q3
df_filtered = df.loc[(df["Gold"] > 0) & (df["Gold.1"]>0) ]
#print( df_filtered.iloc[:,[1,6]])
s = (df_filtered["Gold"] - df_filtered["Gold.1"])/ (df_filtered["Gold"] + df_filtered["Gold.1"])
df2 = s.to_frame(name='Gold_prop')
print(df2.Gold_prop.idxmax())
#Q4
Points = df["Gold.2"]*3 + df["Silver.2"]*2 + df["Bronze.2"]
###################################################################
#Part2
census_df = pd.read_csv('census.csv')
##Q5
by_state = census_df[census_df["SUMLEV"] == 50].groupby('STNAME')['COUNTY'].count()
df_No_Of_Counties = by_state.to_frame(name='No_Of_Counties')
print(df_No_Of_Counties.No_Of_Counties.idxmax())
##Q6
pop2010 = census_df[census_df["SUMLEV"] == 50].groupby('STNAME')['POPESTIMATE2010'].apply(lambda x: x.nlargest(3).sum()).nlargest(3).index.values.tolist()
#print(pop2010)
##Q7
def find_abs_change(x):
    return abs(max(x) - min(x))

x = census_df[census_df["SUMLEV"] == 50].iloc[:,[6,9,10,11,12,13,14]]
y = x.set_index(['CTYNAME'])
#print(y.index.values)   
z= y.apply(find_abs_change, axis=1).idxmax()
print(z)
##Q8

m = census_df[(census_df["SUMLEV"] == 50)  & ((census_df["REGION"] == 1) | (census_df["REGION"] == 2)) & (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014'])]
startswithWash = m['CTYNAME'].apply(lambda x:x.startswith("Washington"))
n = m.where(startswithWash)
n = n.dropna()
h = n[['STNAME','CTYNAME']]

print(m.head())
print(h)