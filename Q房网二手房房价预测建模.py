import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

# 数据预处理
# -----------------------------------------------------------------------------------------------------
houses = pd.read_csv(r'F:\pythoncode\Q房网二手房源价格.csv')

# Region 特征值处理：将区域错误的数据替换正确的
rg = ['龙岗', '宝安', '福田', '龙华', '罗湖', '南山', '坪山', '盐田', '大鹏新区', '光明区']
houses.loc[~houses['Region'].isin(rg),'Region'] = None
houses = houses.fillna(method='ffill')

# Layout特征值处理：提取‘室’和‘厅’的数量创建新的特征
houses['Layout_room_num'] = houses['Layout'].str.extract('(^\d+).*',expand=False).astype('int64')
houses['Layout_hall_num'] = houses['Layout'].str.extract('^\d+.*?(\d+).*',expand=False).astype('int64')
houses = houses.drop('Layout',axis=1)

# Size特征值处理：去掉文字，保留数值
houses['Size'] = houses['Size'].str.extract('(^\d+).*?',expand=False).astype('int64')

# Floor特征值处理：删除异常值，去掉文字，保留数值
houses = houses.loc[~houses['Floor'].str.contains('共')]
houses = houses.loc[houses['Floor'] != '低层']
houses['Floor'] = houses['Floor'].str.extract('^.*?\/(\d+).*',expand=False).astype('int64')

# Year特征值处理：去掉文字，保留数值
houses['Year'] = houses['Year'].str.extract('(^\d+).*',expand=False).astype('int64')
houses['Year'] = datetime.now().year-houses['Year']

# Price特征值：使用IQR进行异常值检测及处理
Percentile = np.percentile(houses['Price'],[0,25,50,75,100])
IQR = Percentile[3]-Percentile[1]
Uplimit = Percentile[3] + 1.5*IQR
Downlimit = Percentile[1] - 1.5*IQR
houses = houses.loc[(houses['Price']>Downlimit)&(houses['Price']<Uplimit)]

# 对分类变量做独热编码
houses_dummies = pd.get_dummies(houses)

# 查看特征相关性
corr_matrix = houses_dummies.corr()
print(corr_matrix['Price'].sort_values(ascending=False))

# 模型训练
# -----------------------------------------------------------------------------------------------------
# 创建测试集
features = houses_dummies.drop('Price',axis=1)
X = features.values
y = houses_dummies['Price'].values
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)

# 尝试线性回归模型
lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)
y_lin_prediction = lin_reg.predict(X_train)
lin_mse = mean_squared_error(y_train,y_lin_prediction)
lin_rmse = np.sqrt(lin_mse)
print(lin_rmse)

# 尝试决策树模型
tree_reg = DecisionTreeRegressor()
tree_reg.fit(X_train,y_train)
y_tree_prediction = tree_reg.predict(X_train)
tree_mse = mean_squared_error(y_train,y_tree_prediction)
tree_rmse = np.sqrt(tree_mse)
print(tree_rmse)

# 尝试随机森林模型
forest_reg = RandomForestRegressor()
forest_reg.fit(X_train,y_train)
y_forest_prediction = forest_reg.predict(X_train)
forest_mse = mean_squared_error(y_train,y_forest_prediction)
forest_rmse = np.sqrt(forest_mse)
print(forest_rmse)  #

# 使用交叉验证评估三种模型：随机森林表现最好
scores = cross_val_score(tree_reg,X_train,y_train,scoring='neg_mean_squared_error',cv=10)
rmse_scores = np.sqrt(-scores)
print(rmse_scores.mean())

lin_scores = cross_val_score(lin_reg,X_train,y_train,scoring='neg_mean_squared_error',cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
print(lin_rmse_scores.mean())

forest_scores = cross_val_score(forest_reg,X_train,y_train,scoring='neg_mean_squared_error',cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)
print(forest_rmse_scores)

# 使用网格搜索调整随机森林的超参数

param_grid = {
    'n_estimators':range(10,101,10),
    'max_features':range(1,29,2)
}

grid_search = GridSearchCV(forest_reg,param_grid,cv=5,scoring='neg_mean_squared_error')
grid_search.fit(X_train,y_train)
print(grid_search.best_params_)

final_model = grid_search.best_estimator_
final_prediction = final_model.predict(X_test)
final_mse = mean_squared_error(y_test,final_prediction)
final_rmse = np.sqrt(final_mse)
print(final_rmse)