import os
from dt_generator import generate_decision_tree
from dt_conversion import convert_tree_to_text
from dt_model import save_decision_tree 

input_csv_path = input("Please enter the nome of the .csv file for the database: ") + '.csv'
if not os.path.isfile(input_csv_path):
    print(f"The file '{input_csv_path}' was not found. Please check the path and try again.")
else:
    output_tree_txt = input("Please enter the name of the output file for the decision tree: ") + '.txt'
    reg, features = generate_decision_tree(
        input_csv=input_csv_path,
        output_txt=output_tree_txt
    )
    save_decision_tree(reg, features, output_tree_txt)
    output_variable = input("Please enter the name of the output variable for the conversion: ")
    base_name = os.path.splitext(os.path.basename(output_tree_txt))[0]
    convert_tree_to_text(base_name, output_variable)
