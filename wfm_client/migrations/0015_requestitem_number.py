# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-13 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0014_auto_20160908_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestitem',
            name='number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]