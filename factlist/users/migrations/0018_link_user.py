# Generated by Django 2.1 on 2018-09-30 16:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_renamed_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordreset',
            name='until',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 1, 16, 53, 35, 235703, tzinfo=utc)),
        ),
    ]