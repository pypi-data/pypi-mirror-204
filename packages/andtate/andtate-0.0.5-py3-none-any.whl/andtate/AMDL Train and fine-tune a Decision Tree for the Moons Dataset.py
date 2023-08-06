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