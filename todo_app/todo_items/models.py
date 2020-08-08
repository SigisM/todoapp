from django.db import models
import datetime

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title
