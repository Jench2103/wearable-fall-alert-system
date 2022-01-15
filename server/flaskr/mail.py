from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from smtplib import SMTP, SMTP_SSL
import ssl

from flaskr import app

def send_email(subject: str, message: str, to_addr: str) -> None:
    msg = MIMEText(message, 'html')
    msg["Subject"] = subject
    msg['From'] = formataddr((str(Header(app.config['SMTP_SENDER_NAME'], 'utf-8')), app.config['SMTP_SENDER_EMAIL']))
    msg["To"] = to_addr

    if app.config['SMTP_USE_SSL']:
        server = SMTP_SSL(app.config['SMTP_SERVER_URL'], app.config['SMTP_SERVER_PORT'], context=ssl.create_default_context())
    else:
        server = SMTP(app.config['SMTP_SERVER_URL'], app.config['SMTP_SERVER_PORT'])
        if server.has_extn('STARTTLS'):
            server.starttls()

    try:
        server.login(app.config['SMTP_ACCOUNT_USERNAME'], app.config['SMTP_ACCOUNT_PASSWORD'])
        server.send_message(msg)
    except Exception as e:
        print(e)
    finally:
        server.quit()
