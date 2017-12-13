# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wfm_client', '0013_auto_20160616_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitem',
            name='quantity',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
