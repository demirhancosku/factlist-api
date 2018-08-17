# Generated by Django 2.1 on 2018-08-17 19:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0013_file_size_and_extension'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perspective', '0002_related_name_of_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Issue',
            new_name='Topic',
        ),
        migrations.RenameModel(
            old_name='IssueLinks',
            new_name='TopicLink',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='issue',
            new_name='topic',
        ),
        migrations.RenameField(
            model_name='topiclink',
            old_name='issue',
            new_name='topic',
        ),
        migrations.AlterModelTable(
            name='topic',
            table='topics',
        ),
        migrations.AlterModelTable(
            name='topiclink',
            table='topic_links',
        ),
    ]
