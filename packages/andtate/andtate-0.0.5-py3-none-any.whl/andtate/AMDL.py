################### Implement Linear Regression (Diabetes Dataset) ###################
################### P1 ###################

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import datasets

diabetes = datasets.load_diabetes() # load data
diabetes.keys

diabetes.target.shape # target vector shape
diabetes.feature_names # coloumn name

# Seperate train and test data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(diabetes.data,diabetes.target, test_size=0.2, random_state=0)
# There are three steps to model something with sklearn
# 1. Setup the model
model = LinearRegression()
# 2. Use fit
model.fit(X_train, y_train)
# 3. Check the score
model.score(X_test, y_test)
y_pred = model.predict(X_test)
plt.plot(y_test, y_pred, '.')

# plot a line, a perfit predict would all fall on this line
x = np.linspace(0,330,100)
y = x
plt.plot(x,y)
plt.show()



################### Implement Logistic Regression (Iris Dataset) ###################
################### P2 ###################
#https://gist.github.com/netj/8836201 #Remove this line once dataset is downloaded

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data=pd.read_csv("/content/iris.csv")
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


################### Implement Multinomial Logistic Regression (Iris Dataset) ###################
################### P3 ###################

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


################### Implement SVM Classifier (Iris Dataset) ###################
################### P4 ###################

import pandas as pd
from sklearn.datasets import load_iris
iris = load_iris()
iris.feature_names
iris.target_names

df = pd.DataFrame(iris.data,columns=iris.feature_names)
df.head()

df["target"] = iris.target
df.head()

df[df.target==1].head()

df[df.target==2].head()

df['flower_name'] = df.target.apply(lambda x: iris.target_names[x])
df.head()

df[45:55]

df0 = df[:50]
df1 = df[50:100]
df2 = df[100:]
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib','inline')
#plt=xlabel('sepal length (cm)')
#plt=ylabel('sepal width (cm)')
plt.scatter(df0['sepal length (cm)'],df0['sepal width (cm)'],color='green',marker = '+')
plt.scatter(df1['sepal length (cm)'],df1['sepal width (cm)'],color='blue',marker = '.')
plt.show()

#plt = xlabel('petal length (cm)')
#plt = ylabel('petal width (cm)')
plt.scatter(df0['petal length (cm)'],df0['petal width (cm)'],color='green',marker = '+')
plt.scatter(df1['petal length (cm)'],df1['petal width (cm)'],color='blue',marker = '.')
plt.show()

from sklearn.model_selection import train_test_split
X=df.drop(['target','flower_name'],axis='columns')
y=df.target

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2)

len(X_train)

len(X_test)


################### Train and fine-tune a Decision Tree for the Moons Dataset ###################
################### P5 ###################

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import pydotplus 
from sklearn import tree
from IPython.display import Image 
from graphviz import Digraph
from sklearn.datasets import make_moons
dataset =make_moons(n_samples=10000, shuffle=True, noise=0.4, random_state=42)
X,y=dataset
X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2, random_state=42)
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

params = {'max_leaf_nodes': list(range (2,100)), 'min_samples_split' : [2, 3, 4]}
grid_search_cv= GridSearchCV(DecisionTreeClassifier (random_state=42), params, verbose=1, cv=3)
grid_search_cv.fit (X_train, y_train)
grid_search_cv.best_estimator_
from sklearn.tree import export_graphviz
dot_data= tree.export_graphviz (grid_search_cv.best_estimator_, out_file=None, feature_names=None, class_names=None, filled=True)

graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())


################### Train a SVM Regressor on the California Housing Dataset ###################
################### P6 ###################

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import reciprocal,uniform 
import numpy as np

housing = fetch_california_housing()
X = housing["data"]
y = housing["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lin_svr = LinearSVR(random_state=42)
lin_svr.fit(X_train_scaled, y_train)

y_pred = lin_svr.predict(X_train_scaled)
mse = mean_squared_error(y_train, y_pred)
mse

np.sqrt(mse)

from sklearn.svm import SVR
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import reciprocal, uniform

param_distributions = {"gamma": reciprocal(0.001,0.1), "C":uniform(1,10)}
rnd_search_cv = RandomizedSearchCV(SVR(), param_distributions, n_iter = 10, verbose = 2, cv = 3, random_state = 42)
rnd_search_cv.fit(X_train_scaled,y_train)


################### Implement Batch Gradient Descent with Early Stopping for Softmax Regression ###################
################### P7 ###################


from sklearn.metrics import log_loss
from sklearn.metrics import mean_squared_error
from sklearn.base import clone
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

iris=load_iris()
X= iris["data"]
y= iris["target"]

scaler = Pipeline([("poly_feature", PolynomialFeatures(degree=90, include_bias=False)),("std_scaler",StandardScaler())])

X_train,X_val,y_train,y_val = train_test_split(X,y,test_size=0.3,random_state=42)

X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

softmax_reg = LogisticRegression(multi_class="multinomial",solver="lbfgs",C=10,warm_start=True,max_iter = 200)

minimum_val_error = float("inf")
best_epoch = None
best_model = None

i = 0
for epoch in range(1000):
    softmax_reg.fit(X_train,y_train)
    y_val_predict = softmax_reg.predict_proba(X_val)
    val_error = log_loss(y_val,y_val_predict)

    if val_error < minimum_val_error:
        minimum_val_error = val_error
        best_epoch = epoch
        best_model = clone(softmax_reg)

    elif val_error >= minimum_val_error:
        i +=1
        if i == 3:
            break
print(best_model)
print(best_epoch)
print(minimum_val_error)


################### Implement MLP for classification of handwritten digits (MNIST Dataset) ###################
################### P8 ###################

import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
from keras.datasets import mnist

objects = mnist
(train_img, train_lab),(test_img, test_lab) = objects.load_data()
for i in range(20):
    plt.subplot(4,5,i+1)
    plt.imshow(train_img[i], cmap='gray_r')
    plt.title("Digit : {}".format(train_lab[i]))
    plt.subplots_adjust(hspace=0.5)
    plt.axis('off')
print('Training images shape: ', train_img.shape)
print('Testing images shape: ', test_img.shape)
print('How image looks like: ')
print(train_img[0])
plt.hist(train_img[0].reshape(784), facecolor='orange')
plt.title('Pixel vs its intensity', fontsize=16)
plt.ylabel('PIXEL')
plt.xlabel('INTENSITY')
train_img = train_img/255.0
test_img = test_img/255.0
print('How image looks like after normalising: ')
print(train_img[0])

plt.hist(train_img[0].reshape(784), facecolor='orange')
plt.title('Pixel vs its intensity', fontsize=16)
plt.ylabel('PIXEL')
plt.xlabel('INTENSITY')

from keras.models import Sequential
from keras.layers import Flatten,Dense

model= Sequential()
input_layer = Flatten(input_shape=(28,28))
model.add(input_layer)
hidden_layer1= Dense(512, activation = 'relu')
model.add(hidden_layer1)
hidden_layer2= Dense(512, activation = 'relu')
model.add(hidden_layer2)
output_layer = Dense(10, activation='softmax')
model.add(output_layer)

#compiling the sequential model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_img, train_lab, epochs=100)
model.save('project.h5')
loss_and_acc = model.evaluate(test_img, test_lab, verbose=2)
print("Test Loss", loss_and_acc[0])
print("Test Accuracy", loss_and_acc[1])
plt.imshow(test_img[0], cmap='gray_r')
plt.title('Actual Value: {}'.format(test_lab[0]))
prediction = model.predict(test_img)
plt.axis('off')
print('Predicted Value: ', np.argmax(prediction[0]))
if(test_lab[0] == (np.argmax(prediction[0]))):
    print('Successful Prediction')
else:
    print('Unsuccessful prediction')
plt.imshow(test_img[2], cmap='gray_r')
plt.title('Actual value: {}'.format(test_lab[2]))
prediction = model.predict(test_img)
plt.axis('off')
print('Predicted Value:', np.argmax(prediction[2]))
if(test_lab[2]==(np.argmax(prediction[2]))):
    print('Successful prediction')
else:
    print('Unsuccessful prediction')

plt.imshow(test_img[2], cmap='gray_r')
plt.title('Actual Value: {}'.format(test_lab[2]))
prediction = model.predict(test_img)
plt.axis('off')
print('Predicted value: ', np.argmax(prediction[2]))
if(test_lab[2]==(np.argmax(prediction[2]))):
    print('Successful prediction')
else:
    print('Unsuccessful prediction')
    
#make a predictionj for a new image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model

#load and prepare the image
def load_image(filename):
    #load the image
    img = load_img(filename, grayscale=True, target_size=(28,28))
    #convert to array
    img = img_to_array(img)
    #reshape into a single sample with one channel
    img = img.reshape(1,28,28)
    #prepare pixel data
    img = img.astype('float32')
    img = img/255.0
    return img