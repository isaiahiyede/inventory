# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-28 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0030_history_history_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestitem',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
