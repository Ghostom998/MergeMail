import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, file=None, server="127.0.0.1", port="1025"):
    
    # send_to must be a list
    send_to_list = [send_to]

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
            Name=basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)

    smtp = smtplib.SMTP(host=server, port=port)
    smtp.sendmail(send_from, send_to_list, msg.as_string())
    smtp.close()