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

# class Reminder(models.Model):
#     daily_reminder = models.BooleanField(default=False)

# class User(models.Model):
#     username = models.CharField(max_length=20)
#     name = models.CharField(max_length=50)
#     password = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name


# class UserManager(models.Manager):
#     def create_user(self, username):
#         user = self.create(title=username)
#         # do something with the book
#         return user

