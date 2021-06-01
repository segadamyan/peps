import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:

    def __init__(self, mail: str, password: str):
        self.mail = mail
        self.password = password

    def send_mail(self, mail: str, msg: str, server):
        message = MIMEMultipart()
        message["Subject"] = "PEP's Update"
        message["From"] = self.mail
        message["To"] = mail
        message.attach(MIMEText(msg, "plain"))

        server.sendmail(self.mail, mail, message.as_string())

    def send_info(self, users: list, new_peps: list):

        msg = ''
        for pep in new_peps:
            for key, value in pep.items():
                msg = f"{msg}\n{key}: {value}"
            msg = f"{msg}\n"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.mail, self.password)
            for user_mail in [user.mail for user in users]:
                try:
                    self.send_mail(user_mail, msg, server)
                    print(f"[SUCCESS]: mail sent to '{user_mail}'")
                except Exception as exp:
                    print(f"[ERROR]: mail didn't send to {user_mail}\n{exp}")
