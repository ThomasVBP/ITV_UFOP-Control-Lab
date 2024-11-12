import re
from mlp_functions import network_dictionary, write_file

def convert_network(original_name, output_variable):
    network_file = f'{original_name}.txt'
    file_table = f'{original_name}_table.txt'
    destination_file = f'{original_name}_800xA.txt'

    with open(destination_file, 'w') as file: 
        file.write('(*The variables are in the format Nij, where i denotes the layer number, and j denotes the neuron number.*)\n')   
    
    # Extract neural network data
    neural_network, layers = network_dictionary(network_file)
    input_vector = []

    # Create parameter table
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
                        file.write(f'{inputs}\treal\t\tin\tyes\n')

        # Ensure the output variable is not in the input vector
        if output_variable in input_vector:
            print("ERROR: The output variable should be different from the input variables.")
            output_variable = input("Please provide a different output variable: ")

        file.write(f'{output_variable}\treal\t\tout\tyes\n')

    # Generate sizes and parameter vectors
    sizes_vector = [len(layer['Neurons']) for layer in layers]
    search_vector, biases_vector, output_vector = write_file(
        layers, sizes_vector, input_vector, destination_file, 
        neural_network, neural_network['Activation Function'], 
        neural_network['Activation Function of the Output Layer']
    )

    # Update biases in the destination file
    with open(destination_file, 'r') as read_file:
        lines = read_file.readlines()

    for index, bias_value in zip(search_vector, biases_vector):
        for i, line in enumerate(lines):
            if index in line:
                lines[i] = f"{line.strip()}) + {bias_value}; \n"

    with open(destination_file, 'w') as file:
        file.writelines(lines)

    # Add variables to the parameter table
    with open(file_table, 'a') as file:
        file.write('\nVariables:\n')
        for variable, out in zip(search_vector, output_vector):
            file.write(f'{variable.strip()}\treal\tretain\n')
            file.write(f'{out.strip()}\treal\tretain\n')

    # Remove the last line if needed (assumes extra newline handling)
    with open(file_table, 'r') as file:
        lines = file.readlines()
    with open(file_table, 'w') as file:
        file.writelines(lines[:-1])

    # Replace the last output variable in the destination file
    with open(destination_file, 'r') as file:
        lines = file.readlines()
    output_pattern = re.compile(rf'^{re.escape(output_vector[-1])}\b')
    for i, line in enumerate(lines):
        if output_pattern.match(line):
            lines[i] = output_pattern.sub(output_variable, line)
    with open(destination_file, 'w') as file:
        file.writelines(lines)
