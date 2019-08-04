import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import recall_score

# 数据预处理
data = pd.read_csv(r'F:\pythoncode\Hands on machine learning\Hands on machine learning\ML-project\信用卡欺诈检测建模\creditcard.csv')
X = data.drop('Class',axis=1)
y = data['Class']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)

scaler = StandardScaler()   # 标准化处理
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练模型
log_reg = LogisticRegression()
log_reg.fit(X_train_scaled,y_train)

#  使用网格搜索进行参数调优
param_grid = {'C':[0.001,0.01,0.1,1,10,100]}
grid_search = GridSearchCV(log_reg,param_grid,cv=5)
grid_search.fit(X_train_scaled,y_train)
print(grid_search.best_params_)

final_model = grid_search.best_estimator_
final_prediction = final_model.predict(X_test_scaled)
print('test set recall:{:.2f}'.format(recall_score(y_test,final_prediction)))








