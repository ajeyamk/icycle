from __future__ import absolute_import

from celery import task

from django.core.mail import send_mail
from django.shortcuts import render_to_response


@task(name='Send async email')
def send_async_email(subject, body, email_from, email_to, fail_silently=True):
    """
    Sends a simple email
    """
    sent = send_mail(subject, body, email_from, email_to, fail_silently=fail_silently)
    return sent


@task(name='Send async system email')
def send_async_system_email(email_container, fail_silently=True):
    """
    Sends an HTML email with a simple text email body if HTML one fails.
    Makes use of utils.email.email_templates.email_templates.EmailContainer
    """
    template = render_to_response(
        email_container.email_template,
        email_container.context,
        content_type='application/xhtml+xml')
    sent = send_mail(
        subject=email_container.subject,
        message=email_container.message,
        from_email=email_container.from_email,
        recipient_list=email_container.recipient_list,
        html_message=template.content,
        fail_silently=fail_silently)
    return sent


@task(name='adder')
def add(x, y):
    print str(x + y)
    return x + y
