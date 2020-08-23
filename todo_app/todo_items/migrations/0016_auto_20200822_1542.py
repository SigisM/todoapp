# Generated by Django 3.0.2 on 2020-08-22 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0015_todo_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo_groups',
            name='task_group',
        ),
        migrations.AddField(
            model_name='todo',
            name='task_group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='todo_items.Todo_Groups'),
        ),
    ]
