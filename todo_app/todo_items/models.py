from django.db import models
import datetime

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateField(default=datetime.date.today)

    def __str__(self):
<<<<<<< Updated upstream
        return self.title
=======
        return '%s %s' % (self.title, self.task_group)
>>>>>>> Stashed changes
