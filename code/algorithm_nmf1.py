# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 23:12:47 2016

@author: rivulet_li
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np

import nimfa

########## prepare data for regression
##########
## test data [22,24,26,28,30] + [23,25,27,29,31]
orderFile_test1 = './testData_order.csv'
orderFile_test2 = './testData_order2.csv'
dfTempOrder_test1 = pd.read_csv(orderFile_test1,sep=',').fillna(0)
dfTempOrder_test2 = pd.read_csv(orderFile_test2,sep=',').fillna(0)
dfTempOrder_test = pd.concat([dfTempOrder_test1,dfTempOrder_test2])

## demand of prediction
demandInfoFile = './day_timeSlot_to_pridict2.txt'
with open(demandInfoFile) as f:
    lines = f.readlines()
    
dayTimeSlots = [item.replace('\n','') for item in lines[1:]]
days = []
timeSlot = []
for dayTimeSlot in dayTimeSlots:
    temp = map(int,dayTimeSlot.split('-'))
    days.append(temp[2])
    timeSlot.append(temp[3])

## training data
namesOrder = ['Day', 'District', 'timeSlot','orderNum_valid','price_valid','orderNum_invalid','price_invalid']

orderFile_training = './trainingData_order.csv'
dfTempOrder_training = pd.read_csv(orderFile_training,sep=',').fillna(0)


################################################################  

def nmfEuc_HW_Xtraining(X,W,H): ## training as X  (4x21
    X=X
    W=W
    H=H
    for iterate in range(0,800):
        
        H = H*np.dot(W.transpose(),X)/np.dot(np.dot(W.transpose(),W),H)    
        
        W[3:,:] = W[3:,:]*np.dot(X[3:,:],H.transpose())/np.dot(W[3:,:],np.dot(H,H.transpose()))
        
    return W,H


def nmfEuc_HW_Xtest(X_,W_,H_): ## test as X (4x10)
    X=X_
    W=W_
    H=H_
    for iterate in range(0,800):
        
        H = H*np.dot(W[:3,:].transpose(),X[:3,:])/np.dot(np.dot(W[:3,:].transpose(),W[:3,:]),H)
        
    X[3,:] = np.dot(W[3,:],H)
   
    return X,H


def nmfDiv_HW(X,H,W):## strange bug 
    for iterate in range(0,800):
        for p in range(0,10):
            for q in range(0,21):
                H[p,q] = H[p,q]*(np.sum((W[:,p]*X[:,q])/np.dot(W,H[:,q])))/np.sum(W[:,q])
        
        for i in range(3,6):
            for j in range(0,10):
                t = W[i,j]*(np.sum((H[j,:]*X[i,:])/np.dot(W[i,:],H)))/np.sum(H[j,:])
                W[i,j] = t
    
    return H,W
################################################################
BM = np.zeros((len(timeSlot),66,10))
for i in range(0,len(timeSlot)):
    df = dfTempOrder_training.loc[(dfTempOrder_training['timeSlot'] < timeSlot[i]+1)&(dfTempOrder_training['timeSlot'] > timeSlot[i]-4)]
    X_arr = np.array(list(df['orderNum_invalid'])).reshape(21,66,4)
    
    df = dfTempOrder_test.loc[(dfTempOrder_test['timeSlot'] < timeSlot[i])&(dfTempOrder_training['timeSlot'] > timeSlot[i]-4)]    
    W_arr_up = np.array(list(df['orderNum_invalid'])).reshape(10,66,3)
    W_0 = np.absolute(np.random.randn(10,66,1))/100
    W_arr = np.concatenate((W_arr_up,W_0),axis=2)
    
    H_0 = np.absolute(np.random.randn(21,10))/100
    
    

    for k in range(0,1):
        X = X_arr[:,k,:].transpose()    
        W = W_arr[:,k,:].transpose()
        H = H_0.transpose()
        
        
        W1,H1 = nmfEuc_HW_Xtraining(X,W,H)
#        print np.sum(np.absolute(W[3,:]-W1[3,:])),'\t', np.sum(np.absolute(X - np.dot(W1,H1)))
        
#        W2,H2 = nmfEuc_HW_Xtest(W,X,H_0)
#        print np.sum(np.absolute(W[3,:]-W2[3,:])),'\t', np.sum(np.absolute(W2 - np.dot(X,H2)))
        
#        W = basis_W(X,H,W_0)
        
        

#############################


#predict_list = []
#for i in range(0,len(timeSlot)):
#    predict_list = predict_list + BM[i,:,days[i]-22].tolist()
#    
############################ 模型验证 ######################################
#BM_test = np.zeros((len(timeSlot),66,5))
#for i in range(0,len(timeSlot)):
#    df = dfTempOrder_test.loc[dfTempOrder_test['timeSlot'] == timeSlot[i]-K]
#    y_arr = np.array(list(df['orderNum_invalid'])).reshape((66,5))
#    
#    for k in range(0,66):
#        BM_test[i,k,:] = y_arr[k]
#    
#test_list = []
#for i in range(0,len(timeSlot)):
#    test_list = test_list + list(BM_test[i,:,(days[i]-23)/2])
#    
#test_arr_nonzeros = np.array([item for item in test_list if item!=0])
#predict_arr_valid = np.array([item for i,item in enumerate(predict_list) if test_list[i]!=0])
#MAPE = np.sum(np.absolute(test_arr_nonzeros - predict_arr_valid)/test_arr_nonzeros)/(43*66)
#
#print 'ALPHA=',ALPHA,'K=',K,'MAPE=',MAPE
##################################################################
#
#    
#names = ['District','dayTimeSlot','gapPridict']
#df = pd.DataFrame(columns = names)
#df['District'] = range(1,67)*43
#
#temp_list = []
#for item in dayTimeSlots:
#    temp_list = temp_list + [item]*66
#    
#df['dayTimeSlot'] = temp_list
#df['gapPridict'] = predict_list
#df.to_csv('predictResult.csv',index=False)






