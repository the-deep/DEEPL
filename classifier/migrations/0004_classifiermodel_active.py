# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0003_auto_20180501_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiermodel',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]