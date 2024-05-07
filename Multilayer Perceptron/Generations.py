from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import numpy as np

n_features = 5 #inputs

X, y = make_regression(n_samples=100, n_features=n_features, noise=0.1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_networks = 10

def format(number):
    return '{:.15f}'.format(number)

for i in range(num_networks):
    neurons = (n_features,) + tuple(np.random.randint(1, 10, np.random.randint(1, 6)))
    activation_function = 'logistic'
    clf = MLPRegressor(hidden_layer_sizes=neurons, activation=activation_function, max_iter=1000)
    clf.fit(X_train, y_train)
    out_activation_function = clf.out_activation_
    score = clf.score(X_test, y_test)

    with open(f'neural_network_information_{i}.txt', 'w') as file:
        num_layers = len(clf.hidden_layer_sizes) + 2
        file.write(f"Number of layers: {num_layers}\n")
        file.write(f"Activation Function: {activation_function}\n")
        file.write(f"Activation Function of the Output Layer: {out_activation_function}\n")

        for j, (layer, biases) in enumerate(zip(clf.coefs_, clf.intercepts_)):
            if j == len(clf.coefs_):
                file.write(f"Output Layer - Neurons: {clf.n_outputs_}\n")
            else:
                file.write(f"Layer {j} - Neurons: {layer.shape[0]}\n")
                file.write("Weights:\n")
                for neuron_dest in range(layer.shape[0]):
                    file.write(f"Neuron {neuron_dest}:\n")
                    for neuron_src, weight in enumerate(layer[neuron_dest]):
                        file.write(f"    Weight for Neuron {neuron_src}: {format(weight)}\n")
                file.write("Biases:\n")
                for neuron, bias in enumerate(biases):
                    file.write(f"    Bias for Neuron {neuron}: {format(bias)}\n")
                file.write("\n")