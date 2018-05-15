from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders
import docx, csv, os.path, smtplib
from getpass import getpass
import pandas as pd

def GetPwd():
    return getpass("Please Enter Your Password:  ")

class CLI:
    def __init__(self, args):

        # Name of input document
        if '-D' in args:
            NewText = self.getText(os.path.abspath(args['-D']))
        
        # Name of CSV file ; df = Data Frame
        if '-C' in args:
            df = self.getValues(os.path.abspath(args['-C']))

        # Name of new document - for testing only
        # if '-N' in args:
        #     NewDocName = args['-N']

        if '-U' in args:
            myemail = args['-U']

        if '-S' in args:
            subject = args['-S']
        
        # Securely prompt the user for their password
        Pwd = GetPwd()
        
        # send emails
        for index, row in df.iterrows():
            self.send_gmail(
            send_from=myemail,
            Password=Pwd,
            send_to=row['EMAIL'], #dyn
            subject=subject,
            body=self.BuildText(NewText, row.to_dict()), #dyn
            file=row['ATTACHMENT'] #dyn
            )

    # Get text from word document. This text will hold placeholder text such as <<FIRST>> for first names, etc.
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

    def send_gmail(self, send_from, Password, send_to, subject, body, file=None, server='smtp.gmail.com', port=587):
        
        send_to_list = send_to if type(send_to) is list else [send_to]

        msg = MIMEMultipart()
        
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to_list)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename = os.path.split(file)[1]
        #dirname = os.path.dirname(file)
        attachment = open(file, "rb")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        msg.attach(part)
        try:
            server = smtplib.SMTP(server, port)
            server.ehlo()
            server.starttls()
            server.login(send_from, Password)
            text = msg.as_string()
            server.sendmail(send_from, send_to, text)
            server.quit()
            print("Message sent successfully to:  " + send_to)
        except:
            print("Error sending message to:  " + send_to)



