# cog-csv-owl-bridge
This is a CSV to OWL Bridge that converts CSV files to OWL and vice-versa. 

Steps for conversion of CSV files to OWL file :
  1. All the CSV files are contained in an xlsx file.
  2. run the start.py file with the option csv_to_owl and give the path to the corresponding xlsx file 
    Command : python start.py csv_to_owl <xlsx file path>
  
Steps for conversion of OWL file to CSV files :
  1. run the start.py file with the option owl_to_csv and give the path to the owl file 
    Command : python start.py owl_to_csv <owl file path>
  2. output.xlsx is created in the working directory. It contains all the CSV files corresponding to all the axioms present.
  
  
 
