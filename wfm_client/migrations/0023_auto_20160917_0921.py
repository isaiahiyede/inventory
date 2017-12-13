# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-17 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0022_item_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='history',
        ),
        migrations.AddField(
            model_name='stockhistory',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wfm_client.item'),
        ),
    ]