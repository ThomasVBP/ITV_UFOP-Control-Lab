import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

df = pd.read_csv("mass_flow_rate_estimation.csv", header=0)
df = df.replace(',', '.', regex=True)
df = df.astype(float)

X = df[["med10", "sd10"]]
y = df["bal75"]  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

activation_function = 'tanh'
mlp = MLPRegressor(hidden_layer_sizes=(2,), activation=activation_function, max_iter=1000, random_state=42)
mlp.fit(X_train, y_train)

with open('filename.txt', 'w') as file:
    num_layers = len(mlp.hidden_layer_sizes) + 2
    file.write(f"Number of layers: {num_layers}\n")
    file.write(f'Number of neurons in the input layer: {X_train.shape[1]}\n')
    file.write(f"Activation Function: {activation_function}\n")
    file.write(f"Activation Function of the Output Layer: {mlp.out_activation_}\n")
    file.write("\n")
    for j, (layer, biases) in enumerate(zip(mlp.coefs_, mlp.intercepts_)):
        file.write(f"Layer {j + 1} - Neurons: {layer.shape[1]}\n")
        file.write("Weights:\n")
        for neuron_dest in range(layer.shape[1]):
            file.write(f"Neuron {neuron_dest}:\n")
            for neuron_src, weight in enumerate(layer[:, neuron_dest]):
                file.write(f"    Weight from neuron {neuron_src}: {weight:.2f}\n")
        file.write("Biases:\n")
        for neuron, bias in enumerate(biases):
            file.write(f"    Bias from neuron {neuron}: {bias:.2f}\n")
        file.write("\n")
