import sys
import owl_csv_code
import csv_owl_code


if len(sys.argv) != 4:
    print("Usage: python start.py o2c <input_file.owl> <output_filename>")
    sys.exit(1)

arg1=(str)(sys.argv[1])
arg2=(str)(sys.argv[2])
arg3=(str)(sys.argv[3])

if arg1 == "o2c":
    owl_csv_code.main(arg2, arg3)

elif arg1=="c2c":
    csv_owl_code.main(arg2)
    
