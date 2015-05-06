# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_resized.forms
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('starttime', models.DateTimeField(verbose_name='start time', default=datetime.datetime(2015, 5, 6, 11, 46, 52, 819229))),
                ('endtime', models.DateTimeField(verbose_name='end time', default=datetime.datetime(2015, 5, 6, 11, 46, 52, 819229))),
                ('location', models.CharField(max_length=100, default='')),
                ('description', models.CharField(max_length=100, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(blank=True, to='prototypeApp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagefile', django_resized.forms.ResizedImageField(upload_to='images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('events', models.ManyToManyField(blank=True, to='prototypeApp.Event', related_name='members')),
                ('friends', models.ManyToManyField(blank=True, to='prototypeApp.Person', related_name='friends_rel_+')),
                ('groups', models.ManyToManyField(blank=True, to='prototypeApp.Group')),
                ('invitedEvents', models.ManyToManyField(blank=True, to='prototypeApp.Event', related_name='pendingMembers')),
                ('invitedFriends', models.ManyToManyField(blank=True, to='prototypeApp.Person', related_name='pendingFriends')),
                ('profilePicture', models.OneToOneField(null=True, blank=True, to='prototypeApp.Image')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
