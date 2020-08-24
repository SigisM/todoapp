from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail
from .forms import *
# from .views import reminder

@shared_task
def send_email_task3():
    send_mail('Task created!',
    'Congratulations. You have created a New Task',
    'my.todo.apl@gmail.com',
    ['s.milkamanavicius@gmail.com'])
    return None
