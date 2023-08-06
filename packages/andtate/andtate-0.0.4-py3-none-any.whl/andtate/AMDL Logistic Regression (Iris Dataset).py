!git clone https://gist.github.com/8836201.git #Remove this line once used

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data=pd.read_csv("/content/8836201/iris.csv")
print("data head() \n",data.head(),"\n")
print("data shape \n",data.shape,"\n")
print("data head() \n",data.info,"\n")
print("data Columns \n",data.columns,"\n")
print("data.isnull().sum() \n",data.isnull().sum(),"\n")

data1=data.dropna(how="any",axis=0)
print("data1 head() \n",data1.head(),"\n")
print("data1 shape \n",data1.shape,"\n")
print("data1 describe \n",data1.describe,"\n")
print("data1 shape \n",data1.head())

sns.barplot(x="sepal.length",y="variety",data=data)
plt.show()

labels='setosa','versicolor','Virginica'
colors=['red','green','blue']

g=data1.variety.value_counts()
plt.pie(g,labels=labels,colors=colors,autopct='%1.1f%%',shadow=False)
plt.axis('equal')
plt.xticks(rotation=0)
plt.show()

data['sepal.length'].hist()
data['sepal.width'].hist()
plt.show()

data['petal.length'].hist()
data['petal.width'].hist()
plt.show()

X=data[['sepal.length','sepal.width','petal.length','petal.width']]
y=data[['variety']]

X_train,X_test,Y_train,Y_test=train_test_split(X,y,test_size=0.3,random_state=101)
sv=LogisticRegression()
sv.fit(X_train,Y_train)

print("\n",sv.predict(X_test))
#print(sv.score(X_test,Y_test))
print("\nAccuracy: ", sv.score(X_test, Y_test) * 100)