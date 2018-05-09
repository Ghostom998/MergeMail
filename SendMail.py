import smtplib, bz2
import os.path
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, file=None, server="127.0.0.1", port=1025):
    
    # send_to must be a list
    send_to_list = send_to if type(send_to) is list else [send_to]

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    # attach file
    with open(file, "rb") as f:
        part = MIMEApplication(
            f.read(),
            Name=os.path.basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file)
    msg.attach(part)

    smtp = smtplib.SMTP(host=server, port=port)
    smtp.sendmail(send_from, send_to_list, msg.as_string())
    smtp.close()


from email.mime.base import MIMEBase
from email import encoders

def send_gmail(send_from, Password, send_to, subject, body, file=None, server='smtp.gmail.com', port=587):
    
    send_to_list = send_to if type(send_to) is list else [send_to]

    msg = MIMEMultipart()
    
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to_list)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = os.path.split(file)[1]
    dirname = os.path.dirname(file)
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