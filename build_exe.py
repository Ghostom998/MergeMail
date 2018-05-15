from distutils.core import setup
import py2exe

import sys, os, pandas, docx, csv, smtplib, os.path
from getpass import getpass
import smtplib
import os.path
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
try:
    # for Python2
    from Tkinter import *
    from Tkinter import TkFileDialog
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog

from MergeMail import GUI, MergeMail, SendMail


setup(
    windows=['MergeMail\\__init__.py'],
    options={
        'py2exe' : {
            'packages' : ['pandas','tkinter','smtplib','csv','docx','python-docx','email','getpass']
        }
    }
    )