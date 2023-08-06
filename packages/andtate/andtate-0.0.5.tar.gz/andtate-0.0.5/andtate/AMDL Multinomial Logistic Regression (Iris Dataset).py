from sklearn import datasets
import numpy as np
from matplotlib import testing	#For Colab
#from matplotlib import test	#For IDLE
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from matplotlib.colors import ListedColormap

iris=datasets.load_iris()
list(iris.keys())
X=iris["data"][:,3:]
y=(iris["target"]==2).astype(np.int32)

from sklearn.linear_model import LogisticRegression

log_reg=LogisticRegression()
log_reg.fit(X,y)
X_new=np.linspace(0,3,1000).reshape(-1,1)
y_proba=log_reg.predict_proba(X_new)
plt.plot(X_new,y_proba[:,1],"g-",label="Iris=Virginica")
plt.plot(X_new,y_proba[:,0],"g-",label="Non=Virginica")
plt.legend()

log_reg.predict([[1.7],[1.5]])
X=iris["data"][:,(2,3)]  #petal length and width
y=(iris["target"]==2).astype(np.int32)
from sklearn.linear_model import LogisticRegression

log_reg=LogisticRegression(solver="liblinear",random_state=42)
log_reg.fit(X,y)
x0,x1=np.meshgrid(np.linspace(3,7,500).reshape(-1,1),
                  np.linspace(0.8,2.7,200).reshape(-1,1),)
X_new=np.c_[x0.ravel(),x1.ravel()]
y_proba=log_reg.predict_proba(X_new)
plt.figure
plt.plot(X[y==0,0],X[y==0,1],"bs")
plt.plot(X[y==1,0],X[y==1,1],"g^")

zz=y_proba[:,1].reshape(x0.shape)
contour=plt.contour(x0,x1,zz,cmap=plt.cm.brg)

left_right=np.array([2.9,7])
boundary = -(log_reg.coef_[0][0]*left_right+log_reg.intercept_[0])/log_reg.coef_[0][1]

plt.clabel(contour, inline=1, fontsize=12)

plt.plot(left_right,boundary,"k--",linewidth=3)
plt.text(3.5,1.5,"Not Iris-Virginica",fontsize=14,color="b",ha="center")
plt.text(6.5,2.3,"Iris-Virginica",fontsize=14,color="g",ha="center")
plt.axis([2.9,7,0.8,2.7])
plt.xlabel("Petal length",fontsize=14)
plt.ylabel("Petal width",fontsize=14)
plt.show()