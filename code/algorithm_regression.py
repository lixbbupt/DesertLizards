# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:53:04 2016

@author: Administrator
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np


######### verify cluster_map: identical
#########
#
#clusterMapFile_test = '../season_1/test_set_1/cluster_map/cluster_map'
#clusterMapFile_training = '../season_1/training_data/cluster_map/cluster_map'
#
#cluster_map_df_test = pd.read_table(clusterMapFile_test, names=['district_hash', 'district_id'])
#cluster_map_set_test = set(list(cluster_map_df_test['district_hash']))
#cluster_map_dict_test = cluster_map_df_test.set_index('district_hash').to_dict()
#cluster_map_list_test = sorted(cluster_map_dict_test['district_id'].items(), key=lambda x: x[1])
#
#cluster_map_df_training = pd.read_table(clusterMapFile_training, names=['district_hash', 'district_id'])
#cluster_map_set_training = set(list(cluster_map_df_training['district_hash']))
#cluster_map_dict_training = cluster_map_df_training.set_index('district_hash').to_dict()
#cluster_map_list_training = sorted(cluster_map_dict_training['district_id'].items(), key=lambda x: x[1])


########## prepare data for regression
##########

orderFile_test = './testData_order.csv'
orderFile_training = './trainingData_order.csv'
demandInfoFile = './day_timeSlot_to_pridict.txt'

namesOrder = ['Day', 'District', 'timeSlot','orderNum_valid','price_valid','orderNum_invalid','price_invalid']

dfTempOrder_test = pd.read_csv(orderFile_test,sep=',').fillna(0)
dfTempOrder_training = pd.read_csv(orderFile_training,sep=',').fillna(0)

with open(demandInfoFile) as f:
    lines = f.readlines()
    
dayTimeSlots = [item.replace('\n','') for item in lines[1:]]
days = []
timeSlot = []
for dayTimeSlot in dayTimeSlots:
    temp = map(int,dayTimeSlot.split('-'))
    days.append(temp[2])
    timeSlot.append(temp[3])


BM = np.zeros((len(timeSlot),66,9))
for i in range(0,len(timeSlot)):
    df = dfTempOrder_training.loc[dfTempOrder_training['timeSlot'] == timeSlot[i]]
    
    x = np.array(range(1,22)).reshape((21,1))
    x_pridict = np.array(range(22,31)).reshape(9,1)
    y_arr = np.array(list(df['orderNum_invalid'])).reshape((66,21))

#############################
## 此处可尝试不同的回归方法，只需更改第一行代码
##    
#    ridge = linear_model.Ridge(alpha=1)
    clf = linear_model.Lasso(alpha=311.3)
    for k in range(0,66):
        
        clf.fit(x,y_arr[k])
        BM[i,k,:] = clf.predict(x_pridict)
#############################


predict_list = []
for i in range(0,len(timeSlot)):
    predict_list = predict_list + BM[i,:,days[i]-22].tolist()
    
names = ['District','dayTimeSlot','gapPridict']
df = pd.DataFrame(columns = names)
df['District'] = range(1,67)*43

temp_list = []
for item in dayTimeSlots:
    temp_list = temp_list + [item]*66
    
df['dayTimeSlot'] = temp_list
df['gapPridict'] = predict_list
df.to_csv('predictResult.csv',index=False)






