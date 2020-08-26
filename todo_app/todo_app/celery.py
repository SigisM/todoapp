from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.task.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('todo_app')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.timezone = 'Europe/Vilnius'

app.conf.beat_schedule = {
    'daily_morning_reminder': {
        'task': 'todo_items.tasks.daily_morning_reminder',
        'schedule': crontab(minute=0, hour=8, day_of_week="*"),
    },
    'daily_evening_reminder': {
        'task': 'todo_items.tasks.daily_evening_reminder',
        'schedule': crontab(minute=0, hour=16, day_of_week="*"),
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))