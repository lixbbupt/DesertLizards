# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 19:31:04 2016

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

#from collections import Counter

fileDir = '../season_1/training_data/order_data'
clusterMapFile = '../season_1/training_data/cluster_map/cluster_map'
cluster_map_df = pd.read_table(clusterMapFile, names=['district_hash', 'district_id'])
cluster_map_list = list(cluster_map_df['district_hash'])
cluster_map_dict = cluster_map_df.set_index('district_hash').to_dict()
cluster_map_dict = cluster_map_dict['district_id']


resultPath = '../trainingOrderDataProcessed2'
if not os.path.exists(resultPath):
    os.makedirs(resultPath)
   
orderNames = ['order_id','driver_id','passenger_id','start_district_hash','dest_district_hash','Price','Time']
Names = ['District','Day','timeSlot']


def time_to_slot(item): # 将'2016-01-01 09:47:54'转换成对应的时间片
    l1 = item.split(' ')
    l2 = l1[1].split(':')
    l3 = map(int,l2)
    return l3[0]*6+l3[1]/10 + 1

files_list = [f for f in os.listdir(fileDir) if f[0] != '.']

usersActivity_array_invalid = np.zeros((len(cluster_map_list),len(files_list),144))
usersActivity_array_valid = np.zeros((len(cluster_map_list),len(files_list),144))

cluster_map_dict_my = dict((y,x) for x,y in cluster_map_dict.iteritems())

for i in range(0,len(files_list)):
                    
    fileOrderPath = fileDir + '/' + files_list[i]
        
    dfTemp = pd.read_csv(fileOrderPath,sep='\t',names=orderNames,index_col='order_id')
        
    timeList = list(dfTemp['Time'])        
            
    timeList_slot = map(time_to_slot, timeList)
            
    dfTemp['Time'] = timeList_slot        
        
    
    
    print files_list[i]
    
    for k in range(1,67):
        
        district = cluster_map_dict_my[k]          
                
        unit_df = dfTemp.loc[(dfTemp['start_district_hash'] == district) | (dfTemp['dest_district_hash'] == district)]

        invalidOrder_df = unit_df.loc[pd.isnull(unit_df['driver_id'])]                
        validOrder_df = unit_df.loc[pd.notnull(unit_df['driver_id'])]
        
        orderNum_invalid = []
        orderNum_valid = []
        for slot in range(1,145):
            df = invalidOrder_df.loc[invalidOrder_df['Time'] == slot]
            orderNum_invalid.append(len(list(df['passenger_id'])))
                
            df = validOrder_df.loc[validOrder_df['Time'] == slot]
            orderNum_valid.append(len(list(df['passenger_id'])))
    
        usersActivity_array_invalid[k-1,i,:] = np.array(orderNum_invalid)
        usersActivity_array_valid[k-1,i,:] = np.array(orderNum_valid)


np.savetxt("usersActivity_array_invalid.csv", usersActivity_array_invalid.reshape((66,21*144)), delimiter=",")
np.savetxt("usersActivity_array_valid.csv", usersActivity_array_valid.reshape((66,21*144)), delimiter=",")

              