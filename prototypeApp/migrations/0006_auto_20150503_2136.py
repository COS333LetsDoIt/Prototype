# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('prototypeApp', '0005_auto_20150501_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='endtime',
            field=models.DateTimeField(verbose_name='end time', default=datetime.datetime(2015, 5, 3, 21, 36, 16, 445921)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(verbose_name='start time', default=datetime.datetime(2015, 5, 3, 21, 36, 16, 445921)),
            preserve_default=True,
        ),
    ]
