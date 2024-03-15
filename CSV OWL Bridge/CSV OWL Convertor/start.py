import sys
import owl_csv_code
import csv_owl_code
arg1=(str)(sys.argv[1])
arg2=(str)(sys.argv[2])

if arg1=="owl_to_csv":
    owl_csv_code.main(arg2)
elif arg1=="csv_to_owl":
    csv_owl_code.main(arg2)
    
    


