# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-18 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0026_auto_20160918_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='history_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]