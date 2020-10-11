import ssl
import smtplib

def send_email(esmtp: object, esend: str, erecv: str, esubj: str, epwrd: str, ebody: str) -> None:
    message = f"Subject: {esubj}\n{ebody}\n"
    server = smtplib.SMTP(esmtp, 587)
    server.starttls(context = ssl.create_default_context())
    server.login(esend, epwrd)
    server.sendmail(esend, erecv, message)
