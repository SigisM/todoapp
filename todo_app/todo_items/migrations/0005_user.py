# Generated by Django 3.0.2 on 2020-08-08 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_items', '0004_auto_20200806_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
