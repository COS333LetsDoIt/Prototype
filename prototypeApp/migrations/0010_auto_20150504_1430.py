# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('prototypeApp', '0009_auto_20150504_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 4, 14, 30, 37, 332891), verbose_name='end time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 4, 14, 30, 37, 332891), verbose_name='start time'),
            preserve_default=True,
        ),
    ]
