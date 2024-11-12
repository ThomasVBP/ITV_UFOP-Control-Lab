
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

## Installation

Download the repository:
git clone https://github.com/ThomasVPB/MLconverter.git

Install globally in the Python environment:
cd <path_to_library>
pip install .


***

In order to complete the conversion, only the *Main* file needs to be run. Before that, however, one must add a snippet of code into the python file used to generate the machine learning model. The snippet code, with the necessary adjustments, is described in details within the *Main* file.



## Example

To demonstrate the usefulness of the program, the example provided is related to a real industrial operation of a mining circuit (image below). In the given circuit, the ore coming from the mine is processed by a crusher, stored in a silo, then transported thourgh a series of conveyor belts to a pile. The physical belt scale installed in the CB-02 measures the circuit's mass flow rate For control purposes, it would be interesting to have the mass flow rate measurement closer to the feeder. Hence, a soft sensor has been created to infer the circuit's mass flow rate using information of the BC-01 current. 

![Circuit](https://github.com/ThomasVBP/ML_Convertion-Python_To_StructuredText/assets/131695492/e55a1b4d-eb0f-4a49-9ca3-c29ff92e2f0f)

In [Example](src/Example), there is a dataset collected from historical data of the circuit operation. The features are the average and standard deviation of the last 10 current data, and the output is the mass flow rate. Using [generate_DT](src/Example/generate_MLP) and [generate_DT](src/Example/generate_DT), one can create, respectively, a Multilayer Perceptron and a Decision Tree for the given example. Then, one need only to run the corresponding *Main* file to convert the python algorithm into a Structured Text code.

## License

This project is licensed under the terms of the MIT License.
