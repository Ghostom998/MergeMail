try:
    # for Python2
    from Tkinter import *
    from Tkinter import TkFileDialog
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog
import sys, os, pandas
from getpass import getpass
from CLI import CLI
from GUI import GUI

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def main():
    # if the user passes no arguements then run the gui
    if len(sys.argv) == 1:
        root = Tk()
        gui = GUI(root)
        root.mainloop()
    # else run the cli
    else:
        myargs = getopts(sys.argv)
        cli = CLI(myargs)

if __name__ == '__main__':
    main()