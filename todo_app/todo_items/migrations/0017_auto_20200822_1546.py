# Generated by Django 3.0.2 on 2020-08-22 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0016_auto_20200822_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='task_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='todo_items.Todo_Groups'),
        ),
    ]
