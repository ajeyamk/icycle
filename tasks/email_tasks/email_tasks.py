from __future__ import absolute_import

from celery import task

from django.core.mail import send_mail
from django.shortcuts import render_to_response


@task(name='Send async email')
def send_async_email(subject, body, email_from, email_to, fail_silently=True):
    """
    Send a simple async email.
    """
    sent = send_mail(subject, body, email_from, email_to, fail_silently=fail_silently)
    return sent


@task(name='Send async system email')
def send_async_html_email(email_obj, fail_silently=True):
    """
    Send an HTML async email. Refer emailer.py on how to use Email Templates.
    """
    if email_obj['email_template']:
        template = render_to_response(
            email_obj['email_template'],
            email_obj['context'],
            content_type='application/xhtml+xml')

        sent = send_mail(
            subject=email_obj['subject'],
            message=email_obj['message'],
            from_email=email_obj['from_email'],
            recipient_list=email_obj['recipient_list'],
            html_message=template.content,
            fail_silently=fail_silently)
    else:
        sent = send_mail(
            subject=email_obj.subject,
            message=email_obj.message,
            from_email=email_obj.from_email,
            recipient_list=email_obj.recipient_list,
            fail_silently=fail_silently)

    return sent
