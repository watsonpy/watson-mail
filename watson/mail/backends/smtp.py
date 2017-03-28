# -*- coding: utf-8 -*-
import smtplib
from watson.mail.backends import abc


class SMTPMaxRetryError(Exception):
    pass


class SMTP(abc.Base):
    """Send an email via SMTP.
    """

    host = None
    port = None
    username = None
    password = None
    use_ssl = False
    start_tls = False
    kwargs = None
    max_retries = None
    _smtp = None
    _connected = False
    _retries = 1

    def __init__(
            self,
            host='localhost',
            port=25,
            username=None,
            password=None,
            use_ssl=False,
            start_tls=False,
            max_retries=5,
            **kwargs):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.start_tls = start_tls
        self.max_retries = max_retries
        self.kwargs = kwargs

    @property
    def smtp_class(self):
        return smtplib.SMTP if not self.use_ssl else smtplib.SMTP_SSL

    def quit(self):
        if self._smtp:
            try:
                self._smtp.quit()
            except:
                pass
            self._smtp = None

    def send(self, message, should_quit=False, **kwargs):
        self._login()
        from_addr = message.senders.from_.email
        to_addrs = str(message.recipients.to)
        msg = message.prepared.as_string()
        self._retries = 1
        self._send(
            from_addr,
            to_addrs=to_addrs,
            message=msg,
            should_quit=should_quit,
            **kwargs)

    def _send(self, from_addr, to_addrs, message, should_quit, **kwargs):
        try:
            mail = self._smtp.sendmail(
                from_addr=from_addr, to_addrs=to_addrs, msg=message, **kwargs)
        except smtplib.SMTPException as exc:
            if self._retries == self.max_retries:
                raise SMTPMaxRetryError(
                    'Reached maximum retries sending to {})'.format(to_addrs)
                ) from exc
            self._retries += 1
            if isinstance(exc, smtplib.SMTPServerDisconnected):
                self._connected = False
                self._smtp = None
                self._login()
            self._send(
                from_addr,
                to_addrs=to_addrs,
                message=message,
                should_quit=should_quit,
                **kwargs)
        if should_quit:
            self._smtp.quit()
            self._smtp = None
        mail = False
        return mail

    def _login(self):
        if self._connected:
            return
        if not self._smtp:
            self._smtp = self.smtp_class(
                host=self.host, port=self.port, **self.kwargs)
        if self.start_tls:
            try:
                self._smtp.ehlo()
                self._smtp.starttls()
            except smtplib.SMTPServerDisconnected:
                self._smtp = None
                self._login()
        self._smtp.login(self.username, self.password)
        self._connected = True

    def __del__(self):
        self.quit()
