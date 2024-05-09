
# ML converter: Python -> Structured Text



## Description

This is a program that converts machine learning model algorithms built using python into Structured Text algorithms. The motivation of this program is to facilitate and fasten the implementation of machine learning algorithms into an industrial Programmable Logic Controller - PLC.

#### Some important details:

* The machine learning models that are able to be converted are Decision Tree and Multilayer Perceptron. Both can be either regression or classification algorithms. 

* The machine learning algorithm must be originally built using Scikit-learn library.

* The syntax of the generated Structured Text code is compatible with the 800xA software, from ABB.

## How to use it

The program is composed of two folders. [One](Decision Tree/Functions.py) for the convertion of decision tree algorithms, and the other for the convertion of multilayer perceptron algorithms. Each folder is composed of two files: *Main* and *Function*.

*Main* file:

This file performs the conversion of the language of machine learning algorithms.

*Function* file:

This file contains the functions used by the 'Main'. 

***

In order to complete the conversion, only the *Main* file need to be run. Before that, however, one must add a snippet of code into the python file used to generate the machine learning model. The snippet code, with the necessary adjustments, is described in details within the *Main* file.



## Example

To demonstrate the usefulness of the program, the example provided is related to a real industrial operation of a mining circuit (image below). In the given circuit, the ore coming from the mine is processed by a crusher, stored in a silo, then transported thourgh a series of conveyor belts to a pile. The physical belt scale instaled in the CB-02 measures the circuit's mass flow rate For control purposes, it would be interesting to have the mass flow rate measurement closer to the feeder. Hence, a soft sensor has been created to infer the circuit's mass flow rate using information of the BC-01 current. 

![Circuit](https://github.com/ThomasVBP/ML_Convertion-Python_To_StructuredText/assets/131695492/e55a1b4d-eb0f-4a49-9ca3-c29ff92e2f0f)

In DATASET, there is a dataset collected from historical data of the circuit operation. The features are the average and standart deviation of the last 10 current data, and the output is the mass flow rate. Using LINKAR ARQUIVO DENTRO DE PASTA EXAMPLE and LINKAR ARQUIVO DENTRO DE PASTA EXAMPLE, one can create, respectively, a Multilayer Perceptron and a Decision Tree for the given example. Then, one need only to run the corresponding *Main* file to convert the python algorithm into a Structured Text code.

## License
