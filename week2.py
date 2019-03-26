# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:06:47 2019

@author: reem_
"""

import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv("9abdec459774d282548ae937512118898227ed050047737544e860a9.csv") 
#split the by element field
#data["Date"]=  pd.to_datetime(data["Date"])
data["Year"]  = data["Date"].apply(lambda x: x[:4])
data["Month-Day"]  = data["Date"].apply(lambda x: x[5:])
print(data.head())
#Remove 02-29
data = data[data["Month-Day"] != "02-29"]
#split the dataset one for the max temp and one for the min
data_max = data[data["Element"] == 'TMAX']
data_min = data[data["Element"] == 'TMIN']
#df for the min and max without the year 2015
df_temp_max =  data[(data["Element"] == 'TMAX') &  (data["Year"] != '2015')] 
df_temp_min =  data[(data["Element"] == 'TMIN') &  (data["Year"] != '2015')]
#group the dfs by date then get the mean values for each day regardless of the year
df_grouped_max = df_temp_max.groupby('Month-Day', as_index=False)['Data_Value'].mean()
df_grouped_min = df_temp_min.groupby('Month-Day', as_index=False)['Data_Value'].mean()
df_grouped_min.rename( columns={1 :'mean_Temp'}, inplace=True )
#get 2015 data
df_temp_max_2015 =  data[(data["Element"] == 'TMAX') &  (data["Year"] == '2015')] 
df_temp_min_2015 =  data[(data["Element"] == 'TMIN') &  (data["Year"] == '2015')]
df_grouped_max_2015 = df_temp_max_2015.groupby('Month-Day', as_index=False)['Data_Value'].mean()
df_grouped_min_2015 = df_temp_min_2015.groupby('Month-Day', as_index=False)['Data_Value'].mean()

#broken temp in 2015
df_merged_max = df_grouped_max.merge(df_grouped_max_2015,how = 'inner', left_on ='Month-Day', right_on='Month-Day' )
df_merged_max.set_index('Month-Day', inplace = True)
x= df_merged_max.iloc[:,1]
y= df_merged_max.iloc[:,0]

df_broken_max = df_merged_max[x>y].iloc[:,1]

df_merged_min = df_grouped_min.merge(df_grouped_min_2015,how = 'inner', left_on ='Month-Day', right_on='Month-Day' )
df_merged_min.set_index('Month-Day', inplace = True)
x= df_merged_min.iloc[:,1]
y= df_merged_min.iloc[:,0]
df_broken_min = df_merged_min[x<y].iloc[:,1]

df_grouped_max.set_index('Month-Day', inplace = True)
df_grouped_min.set_index('Month-Day', inplace = True)

#df_grouped_max['Month-Day'] = pd.to_datetime(df_grouped_max['Month-Day'], format='%m-%d')
plt.figure()

plt.plot( df_grouped_max['Data_Value'], c = 'red', label = 'High Temp' )
plt.plot( df_grouped_min['Data_Value'], c = 'blue' , label = 'Low Temp')
plt.scatter(df_broken_max.index, df_broken_max, s=1 , label = 'Broken High')
plt.scatter(df_broken_min.index, df_broken_min, c ='black', s=1,  label = 'Broken Low')

plt.xlabel('Month')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Extreme Temperatures of 2015 against 2005-2014\n Near Sherwood, Oregon')

plt.gca().axis([-5, 370, -150, 500])
plt.legend(frameon = False)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.gca().fill_between(range(len(df_grouped_max.index)), 
                       df_grouped_max['Data_Value'], df_grouped_min['Data_Value'], 
                       facecolor='gray', 
                       alpha=0.1)

a = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
b = [i+15 for i in a]

Month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(b, Month_name)          
plt.savefig('temp')
plt.show()
#print(data_max.info())
#print(data_min.info())