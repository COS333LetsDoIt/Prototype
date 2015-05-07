# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('starttime', models.DateTimeField(default=datetime.datetime(2015, 5, 7, 13, 26, 15, 479979), verbose_name='start time')),
                ('endtime', models.DateTimeField(default=datetime.datetime(2015, 5, 7, 13, 26, 15, 480016), verbose_name='end time')),
                ('location', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
                ('reminded', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(to='prototypeApp.Event', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagefile', models.ImageField(upload_to='images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(related_name='members', to='prototypeApp.Event', blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='prototypeApp.Person', blank=True)),
                ('groups', models.ManyToManyField(to='prototypeApp.Group', blank=True)),
                ('invitedEvents', models.ManyToManyField(related_name='pendingMembers', to='prototypeApp.Event', blank=True)),
                ('invitedFriends', models.ManyToManyField(related_name='pendingFriends', to='prototypeApp.Person', blank=True)),
                ('profilePicture', models.OneToOneField(null=True, blank=True, to='prototypeApp.Image')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
