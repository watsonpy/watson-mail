# -*- coding: utf-8 -*-
import smtplib
from watson.mail import backends


class TestSMTP(object):
    def test_smtp_class(self):
        backend = backends.SMTP(use_ssl=True)
        assert backend.smtp_class == smtplib.SMTP_SSL
        backend = backends.SMTP()
        assert backend.smtp_class == smtplib.SMTP
