# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-19 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0012_modify_file_for_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='extension',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
