# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('prototypeApp', '0002_auto_20150507_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 14, 6, 19, 910300), verbose_name='end time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 14, 6, 19, 910255), verbose_name='start time'),
            preserve_default=True,
        ),
    ]
