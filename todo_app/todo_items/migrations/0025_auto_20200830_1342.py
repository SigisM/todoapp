# Generated by Django 3.0.2 on 2020-08-30 10:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_items', '0024_auto_20200830_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='created',
            field=models.DateField(default=datetime.datetime(2020, 8, 30, 13, 42, 27, 682884)),
        ),
        migrations.AlterField(
            model_name='todo',
            name='reminder_date',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 8, 30, 13, 42, 27, 682884)),
        ),
    ]