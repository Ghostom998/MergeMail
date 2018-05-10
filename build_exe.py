from distutils.core import setup
import py2exe
from MergeMail import GUI, MergeMail, SendMail


setup(
    windows=['MergeMail\\__init_-.py'],
    options={
        'py2exe' : {
            'packages' : ['pandas','tkinter','smtplib','csv','docx','python-docx','email','getpass']
        }
    }
    )