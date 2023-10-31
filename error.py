from Interpreter import *
import sys

def typeerror(i, expected):
    print("ERROR at line[{}]: Wrong type. {} type expected.".format(i+1, expected))
    sys.exit()

def syntax(i, expected):
    print("ERROR at line[{}]: Wrong syntax. {} expected".format(i+1, expected))
    sys.exit()

def name(i):
    print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
    sys.exit()

def rangeerror(i):
    print("ERROR at line[{}]: Wrong range. number of times must be over 0".format(i+1))
    sys.exit()

def numerror(i):
    print("ERROR at line[{}]: Wrong number. Number must be over 31".format(i+1))
    sys.exit()
