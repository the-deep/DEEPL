# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-27 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_auth.APIUser'),
        ),
    ]
