# Generated by Django 3.0.2 on 2020-08-06 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0003_auto_20200804_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
