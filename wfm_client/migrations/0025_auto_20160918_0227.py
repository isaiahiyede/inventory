# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-18 02:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0024_auto_20160918_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockhistory',
            name='requestitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wfm_client.requestItem'),
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='requestorder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wfm_client.requestOrder'),
        ),
    ]
