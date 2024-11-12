
# ML converter: Python -> Structured Text
[![DOI](https://zenodo.org/badge/787913706.svg)](https://zenodo.org/doi/10.5281/zenodo.11477492)



## Description

MLconverter is a Python library designed to convert Decision Tree and Multilayer Perceptron models into a Structured Text format. The motivation behind this program is to facilitate and accelerate the implementation of machine learning algorithms in an industrial Programmable Logic Controller (PLC).

## Features:

This library is divided into two modules: the Decision Tree Converter and the Multilayer Perceptron Converter. Both modules include docstrings explaining their structure and functions.

#### Some important details

* The original machine learning algorithm must be built using the Scikit-learn library;

* The converted models can be either regression or classification algorithms;

* The generated Structured Text code syntax is compatible with the PLC model from ABB, Industrial IT 800xA DCS.

## How to use it
#### Input file

A dataset file is expected to generate the machine learning algorithm using the Scikit-learn library. This file must be located in the same directory as the corresponding converter module.

#### Installation

Download the repository:
git clone https://github.com/ThomasVPB/MLconverter.git

Install globally in the Python environment:
cd <path_to_library>
pip install .

#### Running the Code

Once the repository files are downloaded to your machine, you can run the converter from the command prompt or directly in Python. Simply execute the conversion file to perform the algorithm conversion.

###### Via Command Prompt

*# Navigate to the library directory*

cd path\MLconverter

*# Create a virtual environment*

python -m venv env

*# Activate the virtual environment*

For Windows: .\env\Scripts\activate
For macOS/Linux: source env/bin/activate

*# Install the library dependencies*

pip install .

*# Navigate to the folder of the converter you want to use*

cd decision_tree_converter (or multilayer_perceptron_converter)

*# Run the conversion script*

python conversion.py

During the execution of the conversion.py script, you will need to provide the name of the dataset file, the name of the .txt file to store the algorithm information, and the machine learning output variable.

*#Deactivating the Virtual Environment*

After running, remember to deactivate the virtual environment to keep your development environment clean: deactivate

###### Via Python directly

Simply run *conversion.py* directly in Python (e.g., using an IDE like PyCharm, Jupyter, or the Python terminal):

python conversion.py

In this case, the same instructions will be presented to provide the name of the dataset file, the name of the .txt file to store the algorithm information, and the machine learning output variable.

***

After runing the code, the converter software produces two .txt files:
* The model algorithm formatted in the Structured Text syntax;
* A table with information on the input and output parameters needed for variable declaration in the 800xA program.

## Example

To demonstrate the usefulness of the program, the example provided is related to a real industrial operation of a mining circuit (image below). In the given circuit, the ore coming from the mine is processed by a crusher, stored in a silo, then transported thourgh a series of conveyor belts to a pile. The physical belt scale installed in the CB-02 measures the circuit's mass flow rate For control purposes, it would be interesting to have the mass flow rate measurement closer to the feeder. Hence, a soft sensor has been created to infer the circuit's mass flow rate using information of the BC-01 current. 

![Circuit](https://github.com/ThomasVBP/ML_Convertion-Python_To_StructuredText/assets/131695492/e55a1b4d-eb0f-4a49-9ca3-c29ff92e2f0f)

In [Example](src/Example), there is a dataset collected from historical data of the circuit operation. The features are the average and standard deviation of the last 10 current data, and the output is the mass flow rate. Using [generate_DT](src/Example/generate_MLP) and [generate_DT](src/Example/generate_DT), one can create, respectively, a Multilayer Perceptron and a Decision Tree for the given example. Then, one need only to run the corresponding *Main* file to convert the python algorithm into a Structured Text code.

## License

This project is licensed under the terms of the MIT License.
