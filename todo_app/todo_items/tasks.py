from celery import shared_task
from celery.task import task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from celery.task import periodic_task
from celery import Celery
from django.core.mail import send_mail
import datetime

from .models import Todo

app = Celery()

app.conf.timezone = 'Europe/Vilnius'

@shared_task
def one_off_task_reminder(subject, body, email):
    send_mail(subject,
    body,
    'my.todo.apl@gmail.com',
    [email])
    return None


@app.task
def daily_evening_reminder():
    users = User.objects.all()
    for user in users:
        list_of_task = []
        todos = Todo.objects.filter(author=user, completed=False, created=datetime.datetime.today())
        for todo in todos:
            list_of_task.append(todo.title)
        nl = '\n'
        subject = (f"Hey {user}. You have uncompleted tasks left for today!")
        msg = (f"Don't forget about your uncompleted today's tasks:\n{nl.join(map(str, list_of_task))}")
        if len(list_of_task)>0:
            send_mail(subject,
            msg,
            'my.todo.apl@gmail.com',
            [user.email])


@app.task
def daily_morning_reminder():
    users = User.objects.all()
    for user in users:
        list_of_task = []
        todos = Todo.objects.filter(author=user, completed=False, created=datetime.datetime.today())
        for todo in todos:
            list_of_task.append(todo.title)
        nl = '\n'
        subject = (f"Hey {user}. You have tasks waiting for you today!")
        msg = (f"For today your tasks are:\n{nl.join(map(str, list_of_task))}")
        if len(list_of_task)>0:
            send_mail(subject,
            msg,
            'my.todo.apl@gmail.com',
            [user.email])
