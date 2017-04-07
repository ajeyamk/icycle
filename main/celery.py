from __future__ import absolute_import

from celery import Celery

app = Celery('main',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=[
                    'tasks.email_tasks.email_tasks',
                    'demos.product_similarity.engine.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

CELERY_TIMEZONE = 'UTC'
