from sys import *
from Interpreter import *

if __name__ == '__main__':
    if argv[1][-5:] == ".mono":
        parse(argv[1])
    else:
        print("ERROR: Wrong file extension.")
