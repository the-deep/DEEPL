# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic_modeling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicmodelingmodel',
            name='depth',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topicmodelingmodel',
            name='keywords_per_topic',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topicmodelingmodel',
            name='number_of_topics',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]