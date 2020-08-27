from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Todo_Group(models.Model):
    group_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.group_name


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    daily_reminder = models.BooleanField(blank=True, default=False)
    reminder_time = models.TextField(blank=True)
    custom_reminder = models.BooleanField(blank=True, default=False)
    reminder_date = models.DateField(default=datetime.date.today)
    task_group = models.ForeignKey(Todo_Group, on_delete=models.SET_NULL, null=True, default='1')


    def __str__(self):
        return self.title
    
    # def __unicode__(self):
        # return u"{}".format(self.task_group.group_name)
