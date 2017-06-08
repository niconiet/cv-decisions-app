import smtplib
from email.mime.text import MIMEText
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
import logging
import logging.handlers
import datetime
from django.conf import settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(settings.LOG_FILENAME, 's', 6, 6)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(handler)


class EmailSender:
    """
    Email sender class
    """
    def __init__(self, body_text=None, subject=None, from_addr=None, to_addr=None, cc_addr=None, filename=None):
        """
        class constructor
        :param body_text: str
        :param subject: str
        :param from_addr: str
        :param to_addr: str
        :param cc_addr: str
        :param filename: str
        """
        self._msg = MIMEMultipart()
        self._msg["Subject"] = subject
        self._msg["From"] = from_addr
        if isinstance(to_addr, list):
            self._msg["To"] = ", ".join(to_addr)
        else:
            self._msg["To"] = to_addr
        self._msg["Cc"] = cc_addr
        self._body = MIMEText(body_text)
        self._msg.attach(self._body)
        self._filename = filename
        self._to_addr = to_addr
        self._smtp_server = "smtpint.corp.cablevision.com.ar"

    def send(self):
        """
        Send mail method
        :return: None
        """
        try:
            if self._filename:
                try:
                    fp = open(self._filename, 'rb')
                    att = email.mime.application.MIMEApplication(fp.read(), _subtype="pdf")
                    fp.close()
                    att.add_header("Content-Disposition", "attachment", filename=self._filename)
                    self._msg.attach(att)
                except Exception:
                    raise Exception("No attachment found")
            try:
                s = smtplib.SMTP(self._smtp_server)
                s.sendmail(self._msg["From"], self._to_addr, str(self._msg))
                s.quit()
            except Exception:
                raise Exception("Exception sending email")
        except Exception as e:
            LOGGER.error(str(datetime.datetime.now()) + " - Email send - " + str(e))

