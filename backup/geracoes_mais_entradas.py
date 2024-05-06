from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import numpy as np

# Número de entradas (características)
n_features = 5  # Altere conforme necessário

# Criando um conjunto de dados de regressão linear com múltiplos recursos (inputs) e um valor de saída
X, y = make_regression(n_samples=100, n_features=n_features, noise=0.1, random_state=42)

# Dividindo o conjunto de dados em dados de treino e dados de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_redes = 5

# Função para formatar números sem notação científica
def formatar_numero(numero):
    # Formate o número com 15 casas decimais sem notação científica
    return '{:.15f}'.format(numero)

# Loop para criar e treinar as redes neurais
for i in range(num_redes):
    # Defina o número de neurônios na primeira camada igual ao número de entradas
    neurons = (n_features,) + tuple(np.random.randint(1, 10, np.random.randint(1, 6)))
    
    activation_function = 'logistic'
    
    clf = MLPRegressor(hidden_layer_sizes=neurons, activation=activation_function, max_iter=1000)

    # Treine o modelo
    clf.fit(X_train, y_train)

    # Obtém a função de ativação da camada de saída
    out_activation_function = clf.out_activation_

    # Avalie o modelo
    score = clf.score(X_test, y_test)

    # Salve as informações em um arquivo de texto
    with open(f'informacoes_rede_neural_{i}.txt', 'w') as file:
        num_camadas = len(clf.hidden_layer_sizes) + 2
        file.write(f"Número de camadas: {num_camadas}\n")
        file.write(f"Função de Ativação: {activation_function}\n")
        file.write(f"Função de Ativação da Camada de Saída: {out_activation_function}\n")

        for j, (layer, biases) in enumerate(zip(clf.coefs_, clf.intercepts_)):
            if j == len(clf.coefs_):
                file.write(f"Camada de Saída - Neurônios: {clf.n_outputs_}\n")
            else:
                file.write(f"Camada {j} - Neurônios: {layer.shape[0]}\n")
                file.write("Pesos:\n")
                for neuron_dest in range(layer.shape[0]):
                    file.write(f"Neurônio {neuron_dest}:\n")
                    for neuron_src, weight in enumerate(layer[neuron_dest]):
                        file.write(f"    Peso para Neurônio {neuron_src}: {formatar_numero(weight)}\n")
                file.write("Biases:\n")
                for neuron, bias in enumerate(biases):
                    file.write(f"    Bias para Neurônio {neuron}: {formatar_numero(bias)}\n")
                file.write("\n")