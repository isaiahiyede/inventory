# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-20 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0029_auto_20160920_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='history_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
