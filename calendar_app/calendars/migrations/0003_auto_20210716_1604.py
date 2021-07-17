# Generated by Django 3.1.8 on 2021-07-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_auto_20210715_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='date',
            name='summary',
        ),
        migrations.AddField(
            model_name='summary',
            name='date',
            field=models.ManyToManyField(blank=True, related_name='summary', to='calendars.Date'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.ManyToManyField(blank=True, related_name='event', to='calendars.Date'),
        ),
    ]
