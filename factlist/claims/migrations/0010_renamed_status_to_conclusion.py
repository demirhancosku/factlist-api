# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-17 15:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0009_auto_20180308_0805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claim',
            options={'ordering': ('-id',)},
        ),
        migrations.RenameField(
            model_name='evidence',
            old_name='status',
            new_name='conclusion',
        ),
    ]