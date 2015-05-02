# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prototypeApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(default='', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='invitedEvents',
            field=models.ManyToManyField(related_name='pendingMembers', to='prototypeApp.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='invitedFriends',
            field=models.ManyToManyField(related_name='pendingFriends', to='prototypeApp.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='profilePicture',
            field=models.URLField(default='http://www.clipartbest.com/cliparts/y4c/9jG/y4c9jGMTE.jpeg', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 17, 31, 20, 605395), verbose_name='end time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 17, 31, 20, 605351), verbose_name='start time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='events',
            field=models.ManyToManyField(to='prototypeApp.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='events',
            field=models.ManyToManyField(related_name='members', to='prototypeApp.Event', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='prototypeApp.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(to='prototypeApp.Group', blank=True),
            preserve_default=True,
        ),
    ]
