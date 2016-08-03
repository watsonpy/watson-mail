Usage
=====

At it's core, watson-mail is a wrapper around the smtplib with the added
ability to send emails via Sendmail.

A number of defaults are put in place so that you need to use the least amount
of code as possible to send the email itself.

::

    from watson.mail import backend, Message

Recipients and Senders
~~~~~~~~~~~~~~~~~~~~~~

While the initial Message is constructed with the to, cc, bcc, from and reply
to addresses in the constructor, if you'd like to modify them later on you
can reference each of these via the following (which will return either and Address
object with name and email attributes, or a list of Address objects):

::

    # to, bcc, cc
    from watson.mail import backend, Message
    message = Message(to='user@email.com', cc='user2@email.com', bcc='user3@email.com')
    message.recipients.to[0]  # user@email.com
    message.recipients.cc[0]  # user2@email.com
    # ...

    # to, bcc, cc
    from watson.mail import backend, Message
    message = Message(to='user@email.com', cc='user2@email.com', bcc='user3@email.com')
    message.senders.from_[0]  # user@email.com
    message.recipients.reply_to[0]  # user2@email.com

Adding new recipients and senders is as simple as ``message.recipients.to.add('email@email.com', 'Name')``. The same methods apply to the ``message.senders`` object.

Using SMTP
~~~~~~~~~~

::

    from watson.mail import backends, Message
    # Sending via SMTP
    # NOTE: If 2-factor auth is enabled for gmail, you will need to
    # request an App Password from within Gmail first.
    message = Message(
        to='user@email.com',
        backend=backends.SMTP(
            host='smtp.gmail.com',
            port=587,
            username='user@gmail.com',
            password='password',
            start_ttls=True))
    message.send()


Using Sendmail
~~~~~~~~~~~~~~

::

    from watson.mail import Message
    # There is no need to change the backend, as it will default to sendmail
    # by default
    message = Message(to='user@email.com')
    message.send()


Adding Attachments
~~~~~~~~~~~~~~~~~~

Attachments can be added in the constructor of the Message object, however they
can also be added individually after that.

::

    from watson.mail import Message
    message = Message(to='user@email.com')
    message.attach('/path/to/file')

The command above will attach the file at ``/path/to/file`` to the email (only
once the ``send()`` method is called) and use ``file`` as the name of the
attachment.
