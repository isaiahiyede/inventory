# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-15 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0010_item_created_by_admin_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestitem',
            name='deleted_by',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='requestitem',
            name='edited_by',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='deleted_by',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='requestorder',
            name='edited_by',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]