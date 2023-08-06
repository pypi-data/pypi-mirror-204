Dragonfile library
The dragonfile library provides a set of functions to read, manipulate, and write CSV files. It is designed to work with files that have a specific structure, with a header row and data in columns.

Usage
To use the library, you need to import it:

python

import dragonfile
Initializing the dragonfile object
The dragonfile object is initialized with the following parameters:

dFile: the path to the CSV file to be read or written.
nColumn: the index of the column to be processed in the CSV file.
dSep: the separator character used in the CSV file (default is ,).
coding: the encoding used in the CSV file (default is utf-8).
python

dragon = dragonfile.dragonfile(dFile='my_file.csv', nColumn=0, dSep=',', coding='utf-8')
Reading a CSV file
To read a CSV file and extract a single column, use the readFile function:

python

dictD, nColumn = dragon.readFile()
This will return a dictionary dictD with the column data, and the updated value of nColumn.

To read a CSV file and extract a single column based on a specific condition, use the readFileSetPeriod function:

python

dictD, nColumn = dragon.readFileSetPeriod(varOp0="", varOp1="Valor1", varOp2="Valor2", varOp3="Valor3", varLog0="1", varLog1="6", varLog2="12", twoColumn=False)
This function also allows you to split the data into two columns, and rename the columns, by setting twoColumn to True.

To read a CSV file and rename specific rows in a column, use the readFileRename function:

python

dictD, nColumn = dragon.readFileRename(nameRow=[], renameRow=[])
This function renames rows in the specified column based on the values in nameRow and renameRow.

Writing a CSV file
To write a CSV file from the data in the dictD dictionary, use the fileToCsv function:

python

dragon.fileToCsv()
This will write the dictionary data to the CSV file specified in the dragonfile object initialization.

Getting the number of columns in a CSV file
To get the number of columns in a CSV file, use the lenColumns function:

python

nColumns = dragon.lenColumns()