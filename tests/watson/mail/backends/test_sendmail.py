# -*- coding: utf-8 -*-
from watson.mail import Message, backends


class TestSendmail(object):
    def test_send(self):
        backend = backends.Sendmail()
        message = Message(
            'test@test.com',
            cc='test@cc.com',
            bcc='test@bcc.com',
            subject='Testing',
            body='Test',
            backend=backend)
        command, message_string = backend._prepare_command('sendmail', message)
        assert command == 'sendmail test@test.com'
