"""
Use the Emailer wrapper class to configure and send an HTML email.

Properties:

    subject: Subject of the email. Should be a string.
    message: Text message in case client does not support HTML messages. Should be a string.
    recipient_list: List of recipient emails. Should be a list of strings.
    email_template: The HTML template to be rendered. Should be a string.
    context: The context for the email template. Should be dict

Methods:

    send_email(): The method which sends the email.

    Properties:

        send_async: If True, email will be sent via celery, else in the main thread.
        Always returns 1.
        fail_silently: If should raise exception on error. Returns 1 if successful.

Usage:

    from tasks.email_tasks.emailer import Emailer

    Emailer(
        subject='subject',
        message='message',
        recipient_list=['sendto@somecompany.com'],
        email_template='email_templates/test_template.html',
        context={'foo': 'BATMAN'}).send_email(send_async=False, fail_silently=True)
"""

from .email_tasks import send_async_html_email

from django.conf import settings


class EmailValidationError(Exception):
    def __init__(self, message):
        super(EmailValidationError, self).__init__(message)


class Emailer(object):
    def __init__(self, subject='', message='', from_email=settings.EMAIL_FROM, recipient_list=[], email_template=None, context=None):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.email_template = email_template
        self.context = context

    def send_email(self, send_async=True, fail_silently=False):
        if self.recipient_list is None:
            raise EmailValidationError('Recipient list cannot be empty')
        # Create the email object
        email_obj = {
            'subject': self.subject,
            'message': self.message,
            'from_email': self.from_email,
            'recipient_list': self.recipient_list,
            'email_template': self.email_template,
            'context': self.context}
        if send_async:
            send_async_html_email.delay(email_obj, fail_silently)
            return 1
        else:
            return send_async_html_email(email_obj, fail_silently)


class TestEmailer(Emailer):
    subject = 'Test mail'
    message = 'Some test body.'
    email_template = 'email_templates/test_template.html'
