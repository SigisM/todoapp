# Generated by Django 3.0.2 on 2020-08-30 10:37

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0023_auto_20200829_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.AlterField(
            model_name='todo',
            name='created',
            field=models.DateField(default=datetime.datetime(2020, 8, 30, 13, 37, 48, 451852)),
        ),
        migrations.AlterField(
            model_name='todo',
            name='reminder_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 8, 30, 13, 37, 48, 451852)),
        ),
    ]