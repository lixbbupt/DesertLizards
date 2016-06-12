
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 21:06:05 2016
统计订单信息，输出每个区域每个时间片的有效订单数量，空订单数量，
以及有效订单均价，空订单均价。每天的统计信息输出到一个文件。
@author: lenovo
"""
import pandas as pd
import numpy as np
import os

#from collections import Counter

fileDir = '../season_1/training_data/order_data'
clusterMapFile = '../season_1/training_data/cluster_map/cluster_map'

resultPath = '../trainingOrderDataProcessed'
if not os.path.exists(resultPath):
    os.makedirs(resultPath)


   
orderNames = ['order_id','driver_id','passenger_id','start_district_hash','dest_district_hash','Price','Time']
Names = ['orderNum_valid','price_valid','orderNum_invalid','price_invalid']
region = set()

def time_to_slot(item): # 将'2016-01-01 09:47:54'转换成对应的时间片
    l1 = item.split(' ')
    l2 = l1[1].split(':')
    l3 = map(int,l2)
    return l3[0]*6+l3[1]/10 + 1


for filename in os.listdir(fileDir):
    
    if filename[0] != '.':
                
        fileOrderPath = fileDir + '/' + filename
        
        dfTemp = pd.read_csv(fileOrderPath,sep='\t',names=orderNames,index_col='order_id')
        
        timeList = list(dfTemp['Time'])        
            
        timeList_slot = map(time_to_slot, timeList)
            
        dfTemp['Time'] = timeList_slot
        
        startDistrict_list = sorted(set(list(dfTemp['start_district_hash'])))
        
        price_invalid = []
        price_valid = []
        orderNum_invalid = []
        orderNum_valid = []
        
        
        for district in startDistrict_list:
            
            print filename + '\t' + district
            
            for slot in range(1,145):
                
                unit_df = dfTemp.loc[(dfTemp['start_district_hash'] == district) & (dfTemp['Time'] == slot)]

                invalidOrder_df = unit_df.loc[pd.isnull(unit_df['driver_id'])]                
                
                validOrder_df = unit_df.loc[pd.notnull(unit_df['driver_id'])]
        
                priceMean_invalid = invalidOrder_df['Price'].mean()
                price_invalid.append(priceMean_invalid)
                
                priceMean_valid = validOrder_df['Price'].mean()
                price_valid.append(priceMean_valid)
                
                ordersCount_invalid = len(list(invalidOrder_df['driver_id']))
                orderNum_invalid.append(ordersCount_invalid)
                
                ordersCount_valid = len(list(validOrder_df['driver_id']))
                orderNum_valid.append(ordersCount_valid)
                
        iterables = [startDistrict_list,range(1,145)]
        index = pd.MultiIndex.from_product(iterables, names=['District', 'timeSlot'])        
        
        dayStatistics_df = pd.DataFrame(np.zeros((144*len(startDistrict_list), 4)), index=index, columns=Names)
        dayStatistics_df['orderNum_valid'] = orderNum_valid
        dayStatistics_df['price_valid'] = price_valid
        dayStatistics_df['orderNum_invalid'] = orderNum_invalid
        dayStatistics_df['price_invalid'] = price_invalid        

        dayStatistics_df.to_csv(resultPath + '/' + filename + '_statistics.cvs',sep='\t')


        
        SS = set(list(dfTemp['start_district_hash']))        
        DS = set(list(dfTemp['dest_district_hash']))       
        print len(SS),len(DS),'\t'        
        region = region|SS|DS
        

##### 将 district_hash 映射为数字
        
cluster_map_df = pd.read_table(clusterMapFile, names=['district_hash', 'district_id'])
cluster_map_set = set(list(cluster_map_df['district_hash']))
cluster_map_dict = cluster_map_df.set_index('district_hash').to_dict()

region_temp = region - cluster_map_set
region_dict = dict(zip(region_temp,range(len(region_temp)+1,len(region)+len(region_temp)+1)))  
region_dict.update(cluster_map_dict)

