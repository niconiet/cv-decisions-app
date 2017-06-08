import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, body_text=None, subject=None, from_addr=None, to_addr=None, cc_addr=None):
        self._msg = MIMEText(body_text)
        self._msg["Subject"] = subject
        self._msg["From"] = from_addr + "@cablevision.com.ar"
        self._msg["To"] = to_addr + "@cablevision.com.ar"
        self._msg["Cc"] = cc_addr

    def send(self):
        try:
            s = smtplib.SMTP("smtpint.corp.cablevision.com.ar")
            s.sendmail(self._msg["From"], [self._msg["To"]], str(self._msg))
            s.quit()
        except Exception as e:
            pass


