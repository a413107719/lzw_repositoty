from sklearn.datasets import load_iris
iris = load_iris()
# Model (can also use single decision tree)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=10)
# Train
model.fit(iris.data, iris.target)
# Extract single tree
estimator = model.estimators_[5]
from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(estimator, out_file='tree.dot',feature_names = iris.feature_names,
                class_names = iris.target_names,rounded = True, proportion = False,
                precision = 2, filled = True)
# Convert to png using system command (requires Graphviz)

# from subprocess import call
# call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
# Display in jupyter notebook
from IPython.display import Image
Image(filename = 'tree.png')



'''
[("RandomForestClassifier, max_features='1'", [0.1344]),
 ("RandomForestClassifier, max_features='2'", [0.1188]),
 ("RandomForestClassifier, max_features='3'", [0.1202]), 
 ("RandomForestClassifier, max_features='4'", [0.1245]), 
 ("RandomForestClassifier, max_features='5'", [0.1259]), 
 ("RandomForestClassifier, max_features='6'", [0.1315]),
 ("RandomForestClassifier, max_features='7'", [0.1287]), 
 ("RandomForestClassifier, max_features='8'", [0.1344]), 
 ("RandomForestClassifier, max_features='9'", [0.1273]), 
 ("RandomForestClassifier, max_features='10'", [0.1358]), 
 ("RandomForestClassifier, max_features='11'", [0.1372]),
 ("RandomForestClassifier, max_features='12'", [0.1414]),
 ("RandomForestClassifier, max_features='13'", [0.1358]), 
 ("RandomForestClassifier, max_features='14'", [0.1344])]
'''