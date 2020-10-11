import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(esmtp: str, esend: str, erecv: str, esubj: str, epwrd: str, ebody: str, eport) -> None:

    # Encode message
    msg = MIMEMultipart()
    msg['From']     = esend
    msg['To']       = erecv
    msg['Subject']  = esubj
    msg.attach(MIMEText(ebody, 'plain'))
    txt = msg.as_string()
    epwrd = epwrd.encode('utf-8')
    esend = esend.encode('utf-8')

    # create SMTP session and start TLS
    server = smtplib.SMTP(esmtp, eport)
    server.starttls()
    server.ehlo()

    # log-in and send e-mail
    server.login(esend, epwrd)
    server.sendmail(esend, erecv, txt)

# i give up
