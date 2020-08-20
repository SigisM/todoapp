from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    daily_reminder = models.BooleanField(blank=True, default=False)
    reminder_time = models.TextField(blank=True)


    def __str__(self):
        return self.title
