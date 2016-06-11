# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:56:21 2016

@author: Administrator
"""

import pandas as pd
import numpy as np
import os


#from collections import Counter
clusterMapFile = '../season_1/test_set_1/cluster_map/cluster_map'
cluster_map_df = pd.read_table(clusterMapFile, names=['district_hash', 'district_id'])
cluster_map_set = set(list(cluster_map_df['district_hash']))
cluster_map_dict = cluster_map_df.set_index('district_hash').to_dict()
cluster_map_dict = cluster_map_dict['district_id']


Days = [22, 24, 26, 28, 30]
#################
## 订单数据处理，生成的cvs文件格式：
## Names = ['Day', 'District', 'timeSlot','orderNum_valid',
##         'price_valid','orderNum_invalid','price_invalid']
#################

statisticsPerDay_dir = '../testOrderDataProcessed'
namesOrder = ['Day', 'District', 'timeSlot','orderNum_valid','price_valid','orderNum_invalid','price_invalid']
namesOrder_int = ['Day', 'District', 'timeSlot','orderNum_valid','orderNum_invalid']
namesOrder_float = ['price_valid','price_invalid']

df = pd.DataFrame(columns = namesOrder)

fileOrder_list =  os.listdir(statisticsPerDay_dir)



for day in range(0,len(fileOrder_list)):
    
    filePathOrder = statisticsPerDay_dir + '/' + fileOrder_list[day]
      
        
    dfTempOrder = pd.read_csv(filePathOrder,sep='\t').fillna(0)
    
    
    District_list_str = list(dfTempOrder['District'])    
    District_list_int = [cluster_map_dict[x] for x in District_list_str]    
    dfTempOrder['District'] = District_list_int
    
    result = dfTempOrder.sort_values(['District', 'timeSlot'], ascending=[1, 1])
    
    result['Day'] = Days[day]
    
    result = result[namesOrder]
    
    df = df.append(result)
    
df[namesOrder_int] = df[namesOrder_int].astype(int)
df[namesOrder_float]=np.round(df[namesOrder_float], decimals=4)
df.to_csv('testData_order.csv',index=False)

##################
##天气数据处理，生成的cvs文件格式：
## Names = ['Day','timeSlot', 'Weather', 'Temperature', 'PM2.5']
##################

weatherData_dir = '../season_1/test_set_1/weather_data'
namesWeather = ['Day','timeSlot', 'Weather', 'Temperature', 'PM2.5']
Names = ['timeSlot', 'Weather', 'Temperature', 'PM2.5']
namesWeather_int = ['Day', 'timeSlot']
namesWeather_float = ['Weather', 'Temperature', 'PM2.5']
def time_to_slot(item): # 将'2016-01-01 09:47:54'转换成对应时间片
    l1 = item.split(' ')
    l2 = l1[1].split(':')
    l3 = map(int,l2)
    return l3[0]*6+l3[1]/10 + 1

fileWeather_list = [f for f in os.listdir(weatherData_dir) if f[0]!='.']

dfTemp = pd.DataFrame(columns = namesWeather)
df = pd.DataFrame(columns = namesWeather)

for day in range(0,len(fileOrder_list)):
    
    dfTemp = pd.DataFrame(columns = namesWeather)
    dfTemp['timeSlot'] = range(1,145)
    dfTemp['Day'] = Days[day]
    dfTemp = dfTemp.set_index(['timeSlot'])
    
    filePathWeather = weatherData_dir + '/' + fileWeather_list[day]    
    dfTempWeather = pd.read_csv(filePathWeather,sep='\t',names=Names)    
    timeList = list(dfTempWeather['timeSlot'])            
    timeList_slot = map(time_to_slot, timeList)            
    dfTempWeather['timeSlot'] = timeList_slot    
    dfTempWeather = dfTempWeather.groupby(dfTempWeather['timeSlot']).mean()
    dfTempWeather[namesWeather_float]=np.round(dfTempWeather[namesWeather_float], decimals=2)  
#    dfTempWeather = dfTempWeather.set_index(['timeSlot'])
    
    dfTemp.update(dfTempWeather,join = 'left', overwrite = False)
    
    dfTemp['timeSlot'] = dfTemp.index
    df = df.append(dfTemp)

df[namesWeather_int] = df[namesWeather_int].astype(int)  
df = df[namesWeather]
df.to_csv('testData_weather.csv',index=False)

##################
##拥堵数据处理，生成的cvs文件格式：
## Names = ['Day', 'District', 'timeSlot', 'level1', 'level2', 'level3', 'level4']
##################

trafficData_dir = '../season_1/test_set_1/traffic_data'
namesTraffic = ['Day', 'District', 'timeSlot', 'level1', 'level2', 'level3', 'level4']
Names = ['District', 'level1', 'level2', 'level3', 'level4', 'timeSlot']
namesTraffic_int = ['Day', 'District', 'timeSlot']

fileTraffic_list = [f for f in os.listdir(trafficData_dir) if f[0]!='.']

dfTemp = pd.DataFrame(columns = namesTraffic)
df = pd.DataFrame(columns = namesTraffic)

for day in range(0,len(fileOrder_list)):
    dfTemp = pd.DataFrame(columns = namesTraffic)
    dfTemp['timeSlot'] = range(1,145)*66
    
    temp_list = []
    for k in range(1,67):
        temp_list = temp_list + [k]*144
        
    dfTemp['District'] = temp_list    
    dfTemp['Day'] = Days[day]
    dfTemp = dfTemp.set_index(['District', 'timeSlot'])
    
    
    filePathTraffic = trafficData_dir + '/' + fileTraffic_list[day]    
    dfTempTraffic = pd.read_csv(filePathTraffic,sep='\t',names=Names)   
    dfTempTraffic['Day'] = day+1
    timeList = list(dfTempTraffic['timeSlot'])            
    timeList_slot = map(time_to_slot, timeList)            
    dfTempTraffic['timeSlot'] = timeList_slot    
    
    District_list_str = list(dfTempTraffic['District'])    
    District_list_int = [cluster_map_dict[x] for x in District_list_str]    
    dfTempTraffic['District'] = District_list_int
    
    dfTempTraffic = dfTempTraffic.sort_values(['District', 'timeSlot'], ascending=[1, 1])
    
    dfTempTraffic['level1'] = map(int,[jam.split(':')[1] for jam in list(dfTempTraffic['level1'])])
    dfTempTraffic['level2'] = map(int,[jam.split(':')[1] for jam in list(dfTempTraffic['level2'])])
    dfTempTraffic['level3'] = map(int,[jam.split(':')[1] for jam in list(dfTempTraffic['level3'])])
    dfTempTraffic['level4'] = map(int,[jam.split(':')[1] for jam in list(dfTempTraffic['level4'])])
    
    dfTempTraffic = dfTempTraffic[namesTraffic]
    dfTempTraffic = dfTempTraffic.set_index(['District', 'timeSlot'])
    
    dfTemp.update(dfTempTraffic,join = 'left', overwrite = False)
    
    dfTemp = dfTemp.reset_index(level=[u'District', u'timeSlot'])
    
    df = df.append(dfTemp)

df[namesTraffic_int] = df[namesTraffic_int].astype(int)  
df = df[namesTraffic]
df.to_csv('testData_traffic.csv',index=False)  

