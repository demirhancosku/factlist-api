# Generated by Django 2.1 on 2018-08-16 15:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='until',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 17, 15, 37, 28, 733465, tzinfo=utc)),
        ),
    ]
