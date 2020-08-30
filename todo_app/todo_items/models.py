from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask
import datetime
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, cronexp
from django.core.validators import MaxValueValidator, MinValueValidator 


# Create your models here.

class Todo_Group(models.Model):
    group_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.group_name


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateField(default=timezone.localtime(timezone.now()).date())
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    daily_reminder = models.BooleanField(blank=True, default=False)
    reminder_time = models.TextField(blank=True)
    custom_reminder = models.BooleanField(blank=True, default=False)
    reminder_date = models.DateField(default=datetime.datetime.today(), blank=True)
    task_group = models.ForeignKey(Todo_Group, on_delete=models.SET_NULL, null=True, default='1')


    def __str__(self):
        return self.title

class CrontabSchedule(CrontabSchedule):

    name = models.CharField(max_length=200)

    def __str__(self):
            return '{3}-{2} on {1}:{0}'.format(
                cronexp(self.minute), cronexp(self.hour),
                cronexp(self.day_of_month), cronexp(self.month_of_year),
                cronexp(self.day_of_week), str(self.timezone)
            )

class Settings(models.Model):
    interval = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.interval
