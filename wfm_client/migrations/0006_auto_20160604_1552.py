# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0005_auto_20160604_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitem',
            name='requestOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wfm_client.requestOrder'),
        ),
    ]
