import re
import numpy as np
from dt_functions import If_Elsif_Insertion, Decreased_indentation, Insertion_terms

def convert_tree_to_text(base_filename, output_variable):
    original_file = base_filename + '.txt'
    destination_file = base_filename + '_800xA.txt'
    table_file = base_filename + '_table.txt'

    # Copy content from source file to destination file
    with open(original_file, 'rb') as original, open(destination_file, 'wb') as destiny:
        destiny.write(original.read())

    # Check tree type
    with open(destination_file, 'r') as destiny:
        content = destiny.read()
    tree_type = 1 if 'class' in content else 2

    # Remove slashes and count them
    with open(destination_file, 'r') as file:
        lines = file.readlines()
    num_slashes = np.array([line.count('|') for line in lines])
    lines = [line.replace('|', '') for line in lines]

    with open(destination_file, 'w') as file:
        file.write(''.join(lines))

    # Insert if and elsif terms
    If_Elsif_Insertion(num_slashes, destination_file)

    # Extract input variables before requesting the output variable
    variables = set()
    with open(destination_file, 'r') as file:
        for line in file:
            if line.strip():
                condition = line.strip().lstrip('if').lstrip('elsif').split(')')[0]
                first_word = condition.split()[0].strip('()')
                if first_word not in ('value', 'class', '---', '') and first_word not in variables:
                    variables.add(first_word)

    # Check if the provided output variable is valid
    while output_variable in variables:
        print("ERROR: The output variable should be different from the input variables.")
        output_variable = input("Please provide a different output variable: ")

    # Adjust syntax and replace variables
    with open(destination_file, 'r') as file:
        content = file.read()

    # Add "then" to if/elsif conditions and wrap conditions in parentheses
    content = re.sub(r'(if|elsif) (.+)', r'\1 (\2) then', content)
    content = re.sub(r'--- ', '', content).replace(':', ' :=')

    # Replace 'class' or 'value' with the output variable depending on tree type
    if tree_type == 1:
        content = re.sub(r'class := (.+)', r'class := \1;', content)
        content = content.replace('class', output_variable)
    elif tree_type == 2:
        content = re.sub(r'value := \[([0-9.]+)\]', r'value := \1;', content)
        content = content.replace('value', output_variable)

    # Write the modified content back to the file
    with open(destination_file, 'w') as file:
        file.write(content)

    # Insert 'end_if' terms and adjust syntax
    index = Decreased_indentation(destination_file)
    calculated_indices, indentation, tabulation = Insertion_terms(destination_file, index)

    with open(destination_file, 'a') as file:
        if tabulation:
            for added_space in reversed(tabulation):
                file.write((' ' * added_space) + 'end_if;' + '\n')
        file.write('end_if;' + '\n')

    # Ensure 'end_if;' is properly inserted at each level of indentation
    with open(destination_file, 'r') as file:
        lines = file.readlines()
    for i in range(len(calculated_indices)):
        line = calculated_indices[i]
        for j in range(len(lines)):
            if j == line:
                lines[j] = (" " * indentation[i]) + 'end_if;' + '\n' + lines[j]

    with open(destination_file, 'w') as file:
        file.write(''.join(lines))

    # Generate the table with input parameters and output variable
    with open(table_file, 'w') as file:
        file.write('Parameters:\n')
        for variable in sorted(variables):
            file.write(f'{variable}\treal\t\tin\tyes\n')
        if tree_type == 1:
            file.write(f'{output_variable}\tdint\t\tout\tyes\n')
        elif tree_type == 2:
            file.write(f'{output_variable}\treal\t\tout\tyes\n')