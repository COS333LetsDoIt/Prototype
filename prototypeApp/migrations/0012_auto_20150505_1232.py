# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('prototypeApp', '0011_auto_20150505_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 5, 12, 32, 5, 176020), verbose_name='end time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 5, 12, 32, 5, 175973), verbose_name='start time'),
            preserve_default=True,
        ),
    ]
