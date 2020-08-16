from celery import shared_task

from django.core.mail import send_mail

@shared_task
def send_email_task():
    send_mail('Task created!',
    'Congratulations. You have created a New Task',
    'my.todo.apl@gmail.com',
    ['s.milkamanavicius@gmail.com'])
    return None
