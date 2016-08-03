# -*- coding: utf-8 -*-
from watson.mail import messages, Message


class TestRecipients(object):
    def test_assigned_recipients(self):
        recipients = messages.Recipients('testing@test.com')
        assert 'testing@test.com' in recipients.to
        assert recipients.to[0].formatted == 'testing@test.com'

    def test_cc_address(self):
        recipients = messages.Recipients('testing@test.com')
        assert 'testing@test.com' in recipients.to
        assert not recipients.bcc
        assert not recipients.cc

    def test_multiple_to_addresses(self):
        recipients = messages.Recipients(
            ['testing@test.com', 'test@test.com'])
        assert len(recipients.to) == 2

    def test_named_recipient(self):
        recipients = messages.Recipients(('Test', 'testing@test.com'))
        assert 'testing@test.com' in recipients.to
        assert recipients.to[0].name == 'Test'
        assert recipients.to[0].formatted == 'Test <testing@test.com>'

    def test_add_remove_recipient(self):
        recipients = messages.Recipients('test@test.com')
        assert len(recipients.to) == 1
        recipients.to.remove('test@test.com')
        assert len(recipients.to) == 0
        assert 'test@test.com' not in recipients.to

    def test_ccs(self):
        recipients = messages.Recipients(
            'test@test.com',
            cc='test@cc.com',
            bcc='test@bcc.com')
        assert len(recipients.cc) == 1
        assert len(recipients.bcc) == 1


class TestSenders(object):
    def test_message_from(self):
        message = Message(to='testing@test.com')
        assert message.senders.from_.email == 'testing@test.com'
        assert 'testing@test.com' in message.senders.reply_to


class TestMailMessage(object):
    def test_message_construction(self):
        message = Message(to='testing@test.com')
        assert repr(message) == '<watson.mail.messages.Message to:1 cc:0 bcc:0>'

    def test_message_prepared(self):
        message = Message(
            to=['testing@test.com', ('Test', 'test@test.com')],
            subject='Testing',
            body='<b>This is a test</b>')
        message_string = message.prepared.as_string()
        assert 'Subject: Testing' in message_string
        assert 'PGI+VGhpcyBpcyBhIHRlc3Q8L2I+' in message_string

    def test_message_raw_prepared(self):
        message = Message(
            to=['testing@test.com', ('Test', 'test@test.com')],
            subject='Testing',
            body='<b>This is a test</b>',
            send_as_base64=False)
        message_string = message.prepared.as_string()
        assert 'This is a test' in message_string

    def test_text_message(self):
        message = Message(
            to='testing@test.com',
            body='<b>This</b> is a test',
            alternative='This is a test')
        message_string = message.prepared.as_string()
        assert 'PGI+VGhpczwvYj4gaXMgYSB0ZXN0' in message_string
        assert 'VGhpcyBpcyBhIHRlc3Q=' in message_string

    def test_text_message_breaks(self):
        message = Message(
            to='testing@test.com',
            body='This<br>is a test')
        message_string = message.prepared.as_string()
        assert 'VGhpcwppcyBhIHRlc3Q=' in message_string

    def test_attachments(self):
        message = Message(to='test@test.com')
        message.attach(__file__)
        assert 'filename="test_mail.py"' in message.prepared.as_string()

    def test_recipients(self):
        message = Message(
            'test@test.com',
            cc='test@cc.com',
            bcc='test@bcc.com')
        message_string = message.prepared.as_string()
        assert 'To: test@test.com' in message_string
        assert 'Cc: test@cc.com' in message_string
        assert 'Bcc: test@bcc.com' in message_string
