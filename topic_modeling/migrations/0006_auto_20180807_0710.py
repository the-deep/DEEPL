# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-07 07:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic_modeling', '0005_auto_20180807_0710'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='topicmodelingmodel',
            unique_together=set([('group_id', 'number_of_topics', 'keywords_per_topic', 'depth')]),
        ),
    ]
