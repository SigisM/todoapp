from celery import shared_task
from celery.task import task
from django.contrib.auth.models import User
from celery import Celery
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask
from django.core.exceptions import ValidationError
from datetime import timedelta
import datetime
import json

from .models import Todo, CrontabSchedule, Settings

app = Celery()

app.conf.timezone = 'Europe/Vilnius'


@shared_task
def send_welcome_word(user, email, password):
    subject = (f"Welcome onboard {user}")
    body = f"""Thank You for registering on Todo App, {user}! \n
        No more missed or forgotten tasks for job, leisure, travel or anything!
        You can now track your daily activities, organize in groups and get daily reminders.\n
        Your login date is:
        Username: {user}
        Password: {password}\n
        You will receive tasks reminders to this email address as well \n\n
        Todo App Team
    """
    send_mail(subject,
    body,
    'my.todo.apl@gmail.com',
    [email])
    return None


@shared_task
def one_off_task_reminder(subject, body, email):
    send_mail(subject,
    body,
    'my.todo.apl@gmail.com',
    [email])
    return None


@shared_task
def delete_reminder(task_id):
    crontabs = CrontabSchedule.objects.all()
    for cron in crontabs:
        if cron.name.startswith("id:"+str(task_id)):
            cron.delete()


@app.task
def delete_old_tasks():
    users = User.objects.all()
    for user in users:
        interval = Settings.objects.get(user=user)
        todos = Todo.objects.filter(author=user, completed=True, created__lt=(datetime.date.today() - datetime.timedelta(days=interval.interval)))
        if todos.exists():
            for todo in todos:
                todo.delete()

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


def custom_reminder(reminder_time, reminder_date, user, task_id, email, title, on_off):
    reminder_hour = reminder_time[0:2]
    reminder_minute = reminder_time[3:5]
    reminder_month = reminder_date[5:7]
    reminder_day = reminder_date[8:10]
    if on_off == True:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=int(reminder_minute),
            hour=int(reminder_hour),
            day_of_week='*',
            day_of_month=int(reminder_day),
            month_of_year=int(reminder_month),
            timezone='Europe/Vilnius',
            name='id'+':'+str(task_id)+'_'+'reminder'+'_'+str(user)+'_'+str(reminder_month)+'_'+str(reminder_day)+'_'+str(reminder_hour)+':'+str(reminder_minute)
            )
        try: 
            PeriodicTask.objects.create(
                crontab=schedule,
                name='id'+':'+str(task_id)+'_'+'reminder'+'_'+str(user)+'_'+str(reminder_month)+'_'+str(reminder_day)+'_'+str(reminder_hour)+':'+str(reminder_minute),
                task='todo_items.tasks.one_off_task_reminder',
                args=json.dumps([title, 'This is a reminder for your task!', email]),
                one_off=True,
                )
        except ValidationError:
            PeriodicTask.objects.get(
                crontab=schedule,
                name='id'+':'+str(task_id)+'_'+'reminder'+'_'+str(user)+'_'+str(reminder_month)+'_'+str(reminder_day)+'_'+str(reminder_hour)+':'+str(reminder_minute),
                task='todo_items.tasks.one_off_task_reminder',
                args=json.dumps([title, 'This is a reminder for your task!', email]),
                one_off=True,
                )
    if on_off == False:
        try:
            periodic_task = PeriodicTask.objects.get(name='id'+':'+str(task_id)+'_'+'Reminder'+'_'+str(user)+'_'+str(reminder_month)+'_'+str(reminder_day)+'_'+str(reminder_hour)+':'+str(reminder_minute))
            periodic_task.delete()
        except:
            pass
