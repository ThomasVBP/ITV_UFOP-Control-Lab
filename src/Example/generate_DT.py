import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree

df = pd.read_csv("mass_flow_rate_estimation.csv", header=0)
df = df.replace(',', '.', regex=True) 
df = df.astype(float)


X = df[['med10', 'sd10']]
y = df['bal75']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

reg = DecisionTreeRegressor(max_depth=3)
reg.fit(X_train, y_train)

feature_names = list(X.columns) 
feature_names=feature_names

with open('filename.txt', 'w') as file:
    file.write(tree.export_text(reg, feature_names=feature_names))
    