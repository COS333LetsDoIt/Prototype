# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('starttime', models.DateTimeField(verbose_name='start time')),
                ('endtime', models.DateTimeField(verbose_name='end time')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(to='prototypeApp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(to='prototypeApp.Event')),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='prototypeApp.Person')),
                ('groups', models.ManyToManyField(to='prototypeApp.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
