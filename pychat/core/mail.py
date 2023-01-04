import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pychat.config import settings


class Email:
    def __init__(
        self,
        subject: str,
        text: str,
        html: str = None,
    ):

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject

        msg_text = MIMEText(text, "plain")
        msg.attach(msg_text)

        if html:
            msg_html = MIMEText(html, "html")
            msg.attach(msg_html)

        self.msg = msg

    def send_mail(self, receiver: str, sender: str = settings.MAIL_FROM):
        with smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
            if settings.MAIL_TLS:
                server.starttls(context=ssl.create_default_context())

            self.msg["From"] = sender
            self.msg["To"] = receiver
            server.login(settings.MAIL_USER, settings.MAIL_PASS)
            server.sendmail(sender, receiver, self.msg.as_string())
