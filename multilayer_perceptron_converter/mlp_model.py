def save_mlp_details(mlp, data, output_model, activation_function):
    with open(output_model, 'w') as file:
        num_layers = len(mlp.hidden_layer_sizes) + 2
        file.write(f"Number of layers: {num_layers}\n")
        file.write(f"Activation Function: {activation_function}\n")
        file.write(f"Activation Function of the Output Layer: {mlp.out_activation_}\n")
        file.write('\n')
        file.write("Input layer:\n")
        for i, variable in enumerate(data.columns[:-1]):
            file.write(f"    Input Neuron {i + 1}: {variable}\n")
        file.write('\n')
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
