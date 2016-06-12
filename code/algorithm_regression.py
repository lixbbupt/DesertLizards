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
demandInfoFile = './day_timeSlot_to_pridict2.txt'

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

ALPHA = 20
K = 0


BM = np.zeros((len(timeSlot),66,10))
for i in range(0,len(timeSlot)):
    df = dfTempOrder_training.loc[dfTempOrder_training['timeSlot'] == timeSlot[i]-K]
    
    x = np.array(range(1,22)).reshape((21,1))
    x_pridict = np.array(range(22,32)).reshape(10,1)
    y_arr = np.array(list(df['orderNum_invalid'])).reshape((66,21))

#############################
## 此处可尝试不同的回归方法，只需更改一行模型的代码
##    
#    clf = linear_model.Ridge(alpha=ALPHA) ## limit； MAPE=2.0 ALPHA = 20000 
#    clf = linear_model.Lasso(alpha=ALPHA) ## limit； MAPE=2.0 ALPHA = 2000
    clf = linear_model.LassoLars(alpha=ALPHA) ## limit； MAPE=2.0 ALPHA = 20
#    clf = linear_model.BayesianRidge(alpha_1=ALPHA,alpha_2=ALPHA) ## limit； MAPE=2.8774 ALPHA = 0.0002
#    clf = LinearRegression() ## MAPE=3.7188
    for k in range(0,66):
        
        clf.fit(x,y_arr[k])
        BM[i,k,:] = clf.predict(x_pridict)
#############################


predict_list = []
for i in range(0,len(timeSlot)):
    predict_list = predict_list + BM[i,:,days[i]-22].tolist()
    
########################### 模型验证 ######################################
BM_test = np.zeros((len(timeSlot),66,5))
for i in range(0,len(timeSlot)):
    df = dfTempOrder_test.loc[dfTempOrder_test['timeSlot'] == timeSlot[i]-K]
    y_arr = np.array(list(df['orderNum_invalid'])).reshape((66,5))
    
    for k in range(0,66):
        BM_test[i,k,:] = y_arr[k]
    
test_list = []
for i in range(0,len(timeSlot)):
    test_list = test_list + list(BM_test[i,:,(days[i]-23)/2])
    
test_arr_nonzeros = np.array([item for item in test_list if item!=0])
predict_arr_valid = np.array([item for i,item in enumerate(predict_list) if test_list[i]!=0])
MAPE = np.sum(np.absolute(test_arr_nonzeros - predict_arr_valid)/test_arr_nonzeros)/(43*66)

print 'ALPHA=',ALPHA,'K=',K,'MAPE=',MAPE
#################################################################

    
names = ['District','dayTimeSlot','gapPridict']
df = pd.DataFrame(columns = names)
df['District'] = range(1,67)*43

temp_list = []
for item in dayTimeSlots:
    temp_list = temp_list + [item]*66
    
df['dayTimeSlot'] = temp_list
df['gapPridict'] = predict_list
df.to_csv('predictResult.csv',index=False)






