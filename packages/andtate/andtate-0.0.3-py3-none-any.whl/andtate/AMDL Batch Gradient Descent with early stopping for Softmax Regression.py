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