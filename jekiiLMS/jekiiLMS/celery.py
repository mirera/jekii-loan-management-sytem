from __future__ import absolute_import, unicode_literals 
import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jekiiLMS.settings')

app = Celery('jekiiLMS')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['jekiiLMS'])

app.conf.beat_schedule = {
    'mark_loans_as_overdue': {
        'task': 'jekiiLMS.tasks.mark_loans_as_overdue',
        'schedule': crontab(minute=0, hour=0),
    },
    'hello_engima': {
        'task': 'jekiiLMS.tasks.hello_engima',
        'schedule': crontab(minute='*'),
    },
    'update_due_amount_task': {
        'task': 'jekiiLMS.tasks.update_due_amount_task',
        'schedule': crontab(minute=0, hour=0),
    },
    'send_loan_balance': {
        'task': 'jekiiLMS.tasks.send_loan_balance',
        'schedule': crontab(hour=9, minute=0, day_of_week=1), #every monday 9am
    },
} 