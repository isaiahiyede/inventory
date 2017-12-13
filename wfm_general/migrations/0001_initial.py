# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-02 17:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password2', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('edited_on', models.DateTimeField(auto_now_add=True)),
                ('deleted_on', models.DateTimeField(auto_now_add=True)),
                ('created_by_admin', models.BooleanField(default=False)),
                ('changed_password', models.BooleanField(default=False)),
                ('profile_up_to_date', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
