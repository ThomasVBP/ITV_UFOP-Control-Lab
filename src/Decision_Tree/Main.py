"""
This file performs the conversion of a decision tree structure (classification 
or regression) generated in Python into a suitable version compatible with the 
'structured text' language used in ABB's 800xA programming software. The goal 
is to streamline the work of engineers in implementing decision trees in an 
industrial environment.

This file was designed considering the syntax of decision trees generated in 
Python using the 'scikit-learn' library and having only a single output. 
Therefore, decision trees that do not meet these requirements may not be 
correctly converted.

A brief description of how the code works:
    
    A .txt file containing the generated decision tree must be saved in the same
    directory as this file. To generate the .txt file, we suggest appending the
    following code at the end of the user-created file used to generate the 
    decision tree.
        
    ---------------------------------------------------------------------------
    with open('filename.txt', 'w') as file:
        file.write(tree.export_text(clf))
        
    NOTE: 
        - Replace 'filename' with the desired name;
        - Replace 'clf' with the name of the variable containing the tree.
    ---------------------------------------------------------------------------
    When starting this code, the user needs to provide the following information:
        1- Name of the .txt file containing the decision tree;
        2- The name of the output variable to be written in the converted tree.
    
    After entering the information, the code within this file, along with the 
    'Functions' file, will generate a .txt file saved in the same directory as 
    this file. The generated file will contain a decision tree that preserves 
    the same functionality as the original decision tree. However, it will have 
    a syntax suitable for the 'structured text' language used by ABB's 800xA 
    software.
    
    Additionally, another file ('tabela.txt') is generated, which contains the 
    variables and parameters used in the code, as well as information such as 
    'Data type', 'Direction', 'FD Port', and 'Attributes'
    
    Thus, users can directly copy the contents of the generated .txt files into 
    the 800xA software, requiring only minimal adjustments if necessary.
    
"""
import numpy as np
import re
from Functions import If_Elsif_Insertion, Decreased_indentation, Insertion_terms

# -------- Input tree information --------            

# -------- Validation of the existence of the .txt file in the folder
while True:
    original_name = input('Source file name: ')
    original_file = original_name + '.txt'

    try:
        # -------- Creating target file -------- 
        destination_file = original_name + '_800xA' + '.txt'
        with open(original_file, 'rb') as original:
            with open(destination_file, 'wb') as destiny:
                destiny.write(original.read())

            break  
    except FileNotFoundError:
        print(f"ATTENTION!\n The file {original_file} does not exist in this folder. Please enter the original file name again.\ndf")

# -------- Checking the tree type (1 = classification | 2 = regression) -------- 

with open(destination_file, 'r') as destiny:   
    content = destiny.read()
if 'class' in content:
    tree_type = 1 
elif 'value' in content:
    tree_type = 2 

# -------- Counting and removal of slashes (|) -------- 

with open(destination_file, 'r') as file:   
    lines = file.readlines()
num_slashes = np.empty(len(lines), dtype=int)
for i in range(len(lines)):
    num_slashes[i] = lines[i].count('|')
    lines[i] = lines[i].replace("|", "")
with open(destination_file, "w") as file:
    file.write(''.join(lines))

# -------- Insertion of If and Elsif -------- 

If_Elsif_Insertion(num_slashes, destination_file)

# -------- Syntax adjustments -------- 

modifications = [("--- ", ""), (":", " :=")]
with open(destination_file, 'r') as file:
    content = file.read()
for from_, to_ in modifications:
    content = content.replace(from_, to_)
with open(destination_file, 'w') as file:
    file.write(content)
    
# -------- Create a list with the names of the input variables and add the name of the output variable --------

variables = set()
with open(destination_file, 'r') as file:
    for line in file:
        if line.strip():
            first_word = line.strip().lstrip('if').lstrip('elsif').split()[0]
            if first_word not in ('value', 'class') and first_word not in variables:
                variables.add(first_word)
    while True:
        output_variable = input("Enter the output variable: ")
        if output_variable not in variables:
            break
        else:
            print("ERROR: The output variable should be different from the input variables. Please provide a different variable.")

# -------- Substituting the input and output variables -------- 

with open(destination_file, "r+") as file:
    content = file.read()    
    if tree_type == 1:
        content = re.sub(r'class := (.+)', r'class := \1;', content)
        content = content.replace('class', output_variable)
    elif tree_type == 2:
        content = re.sub(r'value := \[([0-9.]+)\]', r'value := \1;', content)
        content = content.replace('value', output_variable)
    file.seek(0)
    file.write(content)
    file.truncate() 
    
# -------- Insertion of the term 'end_if' and ';' at the end of the lines -------- 

index = Decreased_indentation(destination_file)
calculated_indices, indentation, tabulation = Insertion_terms(destination_file, index)

with open(destination_file, 'a') as file:
    if tabulation is not None:
        for added_space in reversed(tabulation):
            file.write((' ' * added_space) + 'end_if;' + '\n')
        file.write('end_if;' + '\n')
    else:
        file.write('end_if;' + '\n')

with open (destination_file, 'r') as file:
    lines = file.readlines()   
for i in range(len(calculated_indices)): 
    line = calculated_indices[i]
    for j in range(len(lines)): 
        previous_line = lines[j]
        if j == line: 
            modified_line = (" " * indentation[i]) + 'end_if;' + '\n' + previous_line 
            lines[j] = modified_line         
with open(destination_file, 'w') as file:
    file.write(''.join(lines))
    
# -------- Inclusion of the term 'then' -------- 
    
with open(destination_file, 'r') as file:
    original_text = file.read()   
modified_text = re.sub(r'if (.+)', r'if (\1) then', original_text)
with open(destination_file, 'w') as file:
    file.write(modified_text)
    
# -------- Construction of the variables table -------- 

table_file  = original_name + '_table.txt'
with open(table_file, 'w') as file: 
    file.write('Parameters:\n')
    for variable in variables:
        line = f'{variable}\treal\t\tin\tyes\n'
        file.write(line)
    if tree_type == 1:
        file.write(f'{output_variable}\tdint\t\tout\tyes\n')
    elif tree_type == 2:
        file.write(f'{output_variable}\treal\t\tout\tyes\n')