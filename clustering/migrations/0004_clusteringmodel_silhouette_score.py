# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clustering', '0003_doc2vecmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusteringmodel',
            name='silhouette_score',
            field=models.FloatField(default=-1.0),
        ),
    ]
