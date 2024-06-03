"""
This file performs the conversion of a neural network structure (classification
or regression) generated in Python to a version suitable for the 'structured text' 
language used in ABB's 800xA programming software. The purpose is to streamline 
the work of engineers in implementing neural networks in an industrial environment.

This file was designed considering the syntax of neural networks generated in 
Python using the 'scikit-learn' library, which include multiple neurons in the
input layer, multiple hidden layers with multiple neurons and one neuron in the 
output layer. Therefore, neural networks that do not meet these requirements 
may not be correctly converted.

A brief description of the code's operation:

A .txt file containing information about the generated neural network should be 
saved in the same directory as this file. To generate the .txt file with such 
information, we suggest copying the code below to the end of the user-created 
file used to generate the neural network.
    
    ---------------------------------------------------------------------------        
    with open('filename.txt', 'w') as file:
        num_layers = len(mlp.hidden_layer_sizes) + 2
        file.write(f"Number of layers: {num_layers}\n")
        file.write(f"Activation Function: {activation_function}\n")
        file.write(f"Activation Function of the Output Layer: {mlp.out_activation_}\n")
        file.write('\n')
        file.write("Input layer:\n")
        for i, variable in enumerate(X_train.columns):
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
    
    NOTE:

        - Replace 'filename' with the desired name
        - Replace 'mlp' with the variable name containing the neural network.
    ---------------------------------------------------------------------------
    When initiating this code, the user will need to provide the following 
    information:
        1- Name of the .txt file containing the information of the created neural 
        network;
        3 - Name of the output variable to be written in the converted neural 
        network.
        
        After entering the information, this code will generate a .txt file in 
        the same directory as this code, resulting in a neural network that 
        maintains the same functionality as the original neural network but with 
        syntax adherent to the 'structured text' language used by the ABB 800xA 
        software.

        Additionally, another file ('table.txt') is generated, containing the 
        variables and parameters used in the code, along with information such 
        as 'Data type,' 'Direction,' 'FD Port,' and 'Attributes'.

    
    In this way, it is possible to copy the content of the generated .txt file 
    by this code and paste it directly into the 800xA software, with only the 
    necessary adjustments, such as declaring variables in the 800xA software.

"""
import re
from Functions import network_dictionary, write_file

# -------- Input neural network information --------            

# -------- Validation of the existence of the .txt file in the folder
while True:
    original_name = input('Source file name: ')
    network_file = original_name + '.txt'

    try:
        # -------- Creating table file and destination file-------- 
        file_table = original_name + '_table' + '.txt'   
        destination_file = original_name + '_800xA' + '.txt'
        with open(network_file, 'rb') as original:
            with open(destination_file, 'wb') as destiny:
                destiny.write(original.read())
            break    

    except FileNotFoundError:
        print(f"ATTENTION!\n The file {network_file} does not exist in this folder. Please enter the original file name again.\n")

# ------- Exporting the neural network information from the dictionary -------

neural_network, layers = network_dictionary(network_file)
with open(destination_file, 'w') as file: 
    file.write('(*The variables are in the format Nij, where i denotes the layer number, and j denotes the neuron number.*)\n')

# ------- Checking the number of input variables, the activation function of the overall network and the activation function of the output layer -------

with open (network_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        activation_function = lines[1].split(":")[1].strip()
        out_activation_function = lines[2].split(":")[1].strip() 

## ------- Building the parameter table -------

input_vector = []  
with open(file_table, 'w') as file:
    file.write('Parameters:\n')
    with open(network_file, 'r') as file_in:
        lines = file_in.readlines()
        for line in lines:
           if line.strip().startswith('Input Neuron'):
               parts = line.split(':')
               if len(parts) > 1:
                   inputs = parts[1].strip()
                   input_vector.append(inputs)
                   line = f'{inputs}\treal\t\tin\tyes\n'
                   file.write(line)
    while True:
        output = input("Enter the output variable: ")
        if output not in input_vector:
            break
        else:
            print("ERROR: The output variable should be different from the input variables. Please provide a different variable.")
    file.write(f'{output}\treal\t\tout\tyes\n')
    
num_inputs = len(input_vector)
# ------- Creating a vector with indices containing the number of neurons in each layer -------

sizes_vector = []
for i in range(neural_network['Number of layers'] - 1):
    layer = layers[i]
    neurons = layer['Neurons']
    sizes_vector.append(len(neurons)) 

# ------- Writing the information to the file -------

search_vector, biases_vector, output_vector = write_file(layers, sizes_vector, input_vector, destination_file, neural_network, activation_function, out_activation_function)

# ------- Adding the biases to the file -------

with open(destination_file, 'r') as read_file:
        lines = read_file.readlines()
for index, bias_value in zip(search_vector, biases_vector):
    for i, line in enumerate(lines):
        if index in line:
            lines[i] = f"{line.strip()}) + {bias_value}; \n"
with open(destination_file, 'w') as file:
    file.writelines(lines)

## ------- Building the variable table -------

with open(file_table, 'a') as file:
    file.write('\nVariables:\n')
    for variable, out in zip(search_vector, output_vector):
        line = f'{variable.strip()}\treal\tretain\n'
        file.write(line)
        out_line = f'{out.strip()}\treal\tretain\n'
        file.write(out_line)
with open(file_table, 'r') as file:
    lines = file.readlines()
with open(file_table, 'w') as file:
    file.writelines(lines[:-1]) 

# ------- Inserting the chosen name for the output variable into the file -------
 
with open(destination_file, 'r') as file:
    lines = file.readlines()
default = re.compile(rf'^{re.escape(output_vector[-1])}\b')
for i, line in enumerate(lines):
    if default.match(line):
        lines[i] = default.sub(output, line)
with open(destination_file, 'w') as file:
    file.writelines(lines)