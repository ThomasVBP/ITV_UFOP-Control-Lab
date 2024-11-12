import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

def preprocess_and_generate_mlp(input_csv, output_model, test_size=0.2, random_state=42):
    data = pd.read_csv(input_csv)
    data = data.replace(',', '.', regex=True)
    data = data.astype(float)

    X = data.iloc[:, :-1] 
    y = data.iloc[:, -1]   

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    activation_function = 'tanh'
    mlp = MLPRegressor(hidden_layer_sizes=(2,), activation=activation_function, max_iter=2000, random_state=random_state)
    mlp.fit(X_train, y_train)
    
    return data, mlp, activation_function