
#主要数据见code文件夹中的6个csv文件。

#训练数据

  order,weather,traffic 处理后的信息，生成三个csv文件，包括 [1,2,3,...,21] 共21天的订单、天气、交通信息。

 订单csv文件 trainingData_order.csv ，其数据格式如下：
 
    ['Day', 'District', 'timeSlot','orderNum_valid','price_valid','orderNum_invalid','price_invalid']
    
    >>>> 分别表示日期、区域、时间片、有效订单、有效订单均价、无效订单、无效订单均价
    
    
 天气csv文件 trainingData_weather.csv ，其数据格式如下：
 
    ['Day','timeSlot', 'Weather', 'Temperature', 'PM2.5']
    
     >>>> 分别表示日期、时间片、天气指数、温度、PM2.5
     
     
 交通csv文件 trainingData_traffic.csv ，其数据格式如下：
 
    ['Day', 'District', 'timeSlot', 'level1', 'level2', 'level3', 'level4']
    
    >>>> 分别表示日期、区域、时间片、四个不同级别的拥堵路数（级别越高越拥堵）
 
#测试数据

  order,weather,traffic 处理后的信息，生成三个csv文件，包括 [22,24,26,28,30] 共5天的订单、天气、交通信息（数据含义同上）

 订单csv文件 testgData_order.csv ，其数据格式如下：
 
    ['Day', 'District', 'timeSlot','orderNum_valid','price_valid','orderNum_invalid','price_invalid']
    

 天气csv文件 testData_weather.csv ，其数据格式如下：
 
    ['Day','timeSlot', 'Weather', 'Temperature', 'PM2.5']
    

 交通csv文件 testData_traffic.csv ，其数据格式如下：
 
    ['Day', 'District', 'timeSlot', 'level1', 'level2', 'level3', 'level4']

#### 更新 1

新文件

algorithm_regression.py 该文件用回归方法进行预测，#参数未优化

day_timeSlot_to_pridict.txt 该文件存放要求预测的日期及时间片信息

predictResult.csv 该文件存储回归方法的预测结果，格式符合提交要求

#### 更新 2

algorithm_regression.py 该文件用回归方法进行预测，参数可优化，可计算MAPE

day_timeSlot_to_pridict2.txt 该文件存放要求预测的日期及时间片信息

predictResult.csv 该文件存储回归方法的预测结果，格式符合提交要求
