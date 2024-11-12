import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree

def generate_decision_tree(input_csv, output_txt, test_size=0.3, random_state=42, max_depth=3):
    df = pd.read_csv(input_csv, header=0)
    df = df.replace(',', '.', regex=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()

    features = df.columns[:-1].tolist()
    target = df.columns[-1]
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    reg = DecisionTreeRegressor(max_depth=max_depth)
    reg.fit(X_train, y_train)

    with open(output_txt, 'w') as file:
        file.write(tree.export_text(reg, feature_names=features))