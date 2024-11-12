def network_dictionary(network_file):
    neural_network = {'Layers': []}
    with open(network_file, 'r') as file:
        layers = []
        layer = None 
        for line in file:
            line = line.strip()
            if line.startswith("Number of layers:"):
                neural_network['Number of layers'] = int(line.split(":")[1].strip())
            elif line.startswith("Activation Function:"):
                neural_network['Activation Function'] = line.split(":")[1].strip()
            elif line.startswith("Activation Function of the Output Layer:"):
                neural_network['Activation Function of the Output Layer'] = line.split(":")[1].strip()
            elif line.startswith("Layer"):
                if layer:
                    layers.append(layer)
                layer = {'Neurons': [], 'Biases': {}}
            elif line.startswith("Neuron"):
                neuron = int(line.split(":")[0].split()[-1])
                layer['Neurons'].append({'Neuron': neuron, 'Weights': {}})
            elif line.startswith("Weight from neuron"):
                neuron = int(line.split(":")[0].split()[-1])
                weight = float(line.split(":")[1].strip())
                layer['Neurons'][-1]['Weights'][f'Weight from neuron {neuron}'] = weight
            elif line.startswith("Bias from neuron"):
                neuron = int(line.split(":")[0].split()[-1])
                bias = float(line.split(":")[1].strip())
                layer['Biases'][f'Bias from neuron {neuron}'] = bias
        if layer:
            layers.append(layer)
    neural_network['Layers'] = layers
    return neural_network, layers

def write_file(layers, sizes_vector, input_vector, destination_file, neural_network, activation_function, out_activation_function):
    search_vector = []; biases_vector = []; output_vector = [];
    for i, layer in enumerate(neural_network['Layers']): 
        if i < len(neural_network['Layers']):
            layer = layers[i]
            with open(destination_file, 'a') as file: 
                if i == len(neural_network['Layers']) - 1:
                    file.write('\n(*Input and output information of neurons in the output layer*)\n\n')
                    file.write('(## Calculation of neuron inputs ##)\n\n')
                else: 
                    file.write(f'\n(*Input and output information of neurons in the hidden layer {i+1}*)\n\n')
                    file.write('(## Calculation of neuron input(s) ##)\n')
            neurons = layer['Neurons']; biases = layer['Biases']
            new_vector = [0] * sizes_vector[i] 
            for x in range(len(new_vector)):           
                for j, neuron in enumerate(neurons):
                    if j == x:
                        weight_neurons = neuron['Weights']
                        for weight_key, weight_value in weight_neurons.items():
                            number_neurons = int(weight_key.split()[-1])
                            weight_value = f'{weight_value:.15f}' 
                            with open(destination_file, 'a') as file:
                                if i == len(neural_network['Layers']) - 1 and number_neurons == 0: 
                                    file.write(f'N{i}{number_neurons} := ({input_vector[number_neurons]} * {weight_value}')
                                elif number_neurons == 0:
                                    file.write(f'\nN{i}{x} := ({input_vector[number_neurons]} * {weight_value}')
                                else: 
                                    file.write(f' + {input_vector[number_neurons]} * {weight_value}')
                            key = f'N{i}{x} '
                            if key not in search_vector:
                                search_vector.append(key)                  
            with open(destination_file, 'a') as file: 
                file.write('\n\n(## Output of the neuron(s) - Application of the activation function ##) \n\n')
            for bias_key, bias_value in biases.items():
                biases_vector.append(bias_value)      
            with open(destination_file, 'a') as file: 
                if i == len(layers) - 1:
                    activation = out_activation_function
                else:
                    activation = activation_function
                input_vector.clear()
                for z in range(len(new_vector)):
                    with open(destination_file, 'a') as file:
                        if activation == 'relu':
                            file.write(f'N{i}{z}out := Max(0, N{i}{z});\n')
                        elif activation == 'tanh':
                            file.write(f'N{i}{z}out := (exp(N{i}{z}) - exp(-N{i}{z})) / (exp(N{i}{z}) + exp(-N{i}{z}));\n')
                        elif activation == 'logistic':
                            file.write(f'N{i}{z}out := 1 / (1 + exp(-N{i}{z}));\n')
                        elif activation == 'identity':
                            file.write(f'N{i}{z}out := N{i}{z};\n')
                    input_vector.append(f'N{i}{z}out')
                    output_vector.append(f'N{i}{z}out')
    return search_vector, biases_vector, output_vector