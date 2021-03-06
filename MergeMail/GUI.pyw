try:
    # for Python2
    from Tkinter import *
    from Tkinter import TkFileDialog
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE, formatdate
import docx, csv, os.path, smtplib
import pandas as pd
class ConnectionError(Exception): pass
class AuthError(Exception): pass
class SendError(Exception): pass

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("MergeMail")

        # Doc
        self.doc_label = Label(master, text="Word Document: ")
        self.doc_label.grid(row=0,column=0)
        self.docx_button = Button(master, text="Browse Doc", command=self.browse_button_docx)
        self.docx_button.grid(row=0,column=1)

        # CSV
        self.doc_label = Label(master, text="CSV File: ")
        self.doc_label.grid(row=1,column=0)
        self.docx_button = Button(master, text="Browse CSV", command=self.browse_button_csv)
        self.docx_button.grid(row=1,column=1)

        # Subject
        self.SubjField = StringVar()
        self.subject_label = Label(master, text="Subject: ")
        self.subject_label.grid(row=2,column=0)
        self.subject_entry = Entry(master, textvariable=self.SubjField)
        self.subject_entry.grid(row=2,column=1,sticky=W)

        # Username
        self.UserField = StringVar()
        self.user_label = Label(master, text="Your Gmail: ")
        self.user_label.grid(row=0,column=2)
        self.user_entry = Entry(master, textvariable=self.UserField)
        self.user_entry.grid(row=0,column=3,sticky=W)

        # Password
        self.PassField = StringVar()
        self.pass_label = Label(master, text="Your Password: ")
        self.pass_label.grid(row=1,column=2)
        self.pass_entry = Entry(master, textvariable=self.PassField, show="*")
        self.pass_entry.grid(row=1,column=3,sticky=W)

        # Run Button
        self.run_button = Button(master, text="Run", command=self.button_run)
        self.run_button.grid(row=2,column=2,columnspan=2)

        # Message Box
        self.text = Text(master,wrap=WORD)
        self.text.grid(row=3,column=0,columnspan=4,rowspan=3)

    def browse_button_docx(self):
        filename = filedialog.askopenfile(parent=self.master,mode='rb',title='Choose the word document')
        self.DocName = filename.name
        self.Message("Successfully loaded " + os.path.split(self.DocName)[1])
    
    def browse_button_csv(self):
        filename = filedialog.askopenfile(parent=self.master,mode='rb',title='Choose the csv document')
        self.CsvName = filename.name
        self.Message("Successfully loaded " + os.path.split(self.CsvName)[1])
    
    def button_run(self):
        try:
            NewText = self.getText(os.path.abspath(self.DocName))
            df = self.getValues(os.path.abspath(self.CsvName))
            myemail = self.UserField.get()
            pwd = self.PassField.get()
            subject = self.SubjField.get()
        except Exception as e:
            self.Message(str(e))
        
        for index, row in df.iterrows():
            self.send_guimail(
            send_from=myemail,
            Password=pwd,
            send_to=row['EMAIL'], #dyn
            subject=subject,
            body=self.BuildText(NewText, row.to_dict()), #dyn
            file=row['ATTACHMENT'] #dyn
            )
    
    def send_guimail(self, send_from, Password, send_to, subject, body, file=None, server='smtp.gmail.com', port=587):
        
        send_to_list = send_to if type(send_to) is list else [send_to]

        msg = MIMEMultipart()
        
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to_list)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename = os.path.split(file)[1]
        #dirname = os.path.dirname(file)
        try:
            attachment = open(file, "rb")
        except FileNotFoundError as f:
            self.Message(f)
            self.Message("Attachment not found. Please check that the file exists or has been typed correctly.")
        except Exception as e:
            self.Message(str(e))
            self.Message("Something unexpected happened. Please report the error to our GitHub Page.")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        msg.attach(part)
        text = msg.as_string()

        sender = Mailer(server, port, send_from, Password) # the except SocketError/AuthError could go here
        
        try:
            sender.message(send_to, text)
        except SocketError:
            self.Message("Couldn't connect to server")
        except AuthError:
            self.Message("Invalid username and/or password!")
        else:
            self.Message("Message sent!")

    def getText(self, filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)

    def getValues(self, filename):
        return pd.read_csv(filename)

    # Method build new text based on previous
    def BuildText(self, Text, dic):
        for key, item in dic.items():
            Text = Text.replace("<<" + key + ">>", item)
        return Text
    
    def Message(self, text, pos=END):
        self.text.insert(pos, text + "\n")


class Mailer:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        try:
            self.server = smtplib.SMTP(self.host, self.port)
        except smtplib.socket.gaierror:
            raise ConnectionError("Error connecting to %s" % (self.host))

    def auth(self):
        try:
            self.server.login(self.username, self.password)
        except SMTPAuthenticationError:
            raise AuthError("Invalid username (%s) and/or password" % (self.username))

    def message(self, to, msg):
        try:
            self.server.sendmail(self.username, to, msg)
        except smtplib.socket.gaierror as errormsg:
            raise SendError("Couldn't send message: %s" % (errormsg))
        except smtplib.socket.timeout:
            raise ConnectionError("Socket error while sending message")
