# cog-csv-owl-bridge
This is a CSV to OWL Bridge that converts CSV files to OWL and vice-versa. 

1. Firstly download all the files present in the same folder and run the whole folder as project
2. Then Firstly run the build tool to install the necessary libraries needed for the programme to perform.
3. Place the testing file from the Testing folder with the CSV_to_owl convertor or mention the location of the file in the code and then run the programme.
4. Now when the files are generated you can directly compare them by placing them in the comparison folder or mentioning the files location in the programme and its result will be show. 

Steps for conversion of OWL file to CSV files :
  1. run the start.py file with the option owl_to_csv and give the path to the owl file .
    Command : python start.py owl_to_csv "owl file path".
  2. output.xlsx is created in the working directory. It contains all the CSV files corresponding to all the axioms present.
  
Steps for conversion of CSV files to OWL file :
  1. All the CSV files are contained in an xlsx file.
  2. run the start.py file with the option csv_to_owl and give the path to the corresponding xlsx file 
    Command : python start.py csv_to_owl "xlsx file path".
