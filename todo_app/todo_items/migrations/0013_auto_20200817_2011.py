# Generated by Django 3.0.2 on 2020-08-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0012_auto_20200817_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='reminder_time',
            field=models.DateTimeField(blank=True),
        ),
    ]