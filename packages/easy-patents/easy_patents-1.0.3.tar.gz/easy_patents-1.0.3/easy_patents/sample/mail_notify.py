import os
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
import datetime


def make_mimetext(fromaddr, toaddrs, subject, body):
    jp = 'iso-2022-jp'
    msg = MIMEText(body.encode(jp, "ignore"), 'plain', jp,)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddrs)
    return msg


def send_email(smtp_server, smtp_port, fromaddr, toaddrs, mimetext, is_ssl=False, user=None, password=None):
    if is_ssl:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
    # server.set_debuglevel(2)
    print("LOGIN START", user, password)
    if user:
        server.login(user, password)
    print("LOGIN END")
    server.sendmail(fromaddr, toaddrs, mimetext.as_string())


def email(fromaddr, toaddrs, smtp_server, smtp_port, subject, body, is_ssl=False, user=None, password=None):
    mimetext = make_mimetext(fromaddr, toaddrs, subject, body)
    send_email(smtp_server, smtp_port, fromaddr, toaddrs, mimetext, is_ssl, user, password)


if __name__ == "__main__":
    pass
