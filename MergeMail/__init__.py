import sys, os, pandas
from getpass import getpass
from MergeMail import getText, getValues, BuildText
from SendMail import send_gmail
from GUI import run_gui

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
        run_gui()
    
    # else run the cli
    else:
        myargs = getopts(sys.argv)

        # Name of input document
        if '-D' in myargs:
            NewText = getText(os.path.abspath(myargs['-D']))
        
        # Name of CSV file ; df = Data Frame
        if '-C' in myargs:
            df = getValues(os.path.abspath(myargs['-C']))

        # Name of new document - for testing only
        # if '-N' in myargs:
        #     NewDocName = myargs['-N']

        if '-U' in myargs:
            myemail = myargs['-U']

        if '-S' in myargs:
            subject = myargs['-S']
        
        # Securely prompt the user for their password
        Pwd = getpass("Please Enter Your Password:  ")
        
        # send emails
        for index, row in df.iterrows():
            send_gmail(
            send_from=myemail,
            Password=Pwd,
            send_to=row['EMAIL'], #dyn
            subject=subject,
            body=BuildText(NewText, row.to_dict()), #dyn
            file=row['ATTACHMENT'] #dyn
            )


if __name__ == '__main__':
    main()