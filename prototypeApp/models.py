################################################################################
# models.py
# Contains objects and the relationships between the objects that are
# represented in the database
################################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile

import datetime
from PIL import Image as Img
import StringIO

# Image model contains the image for each profile picture.
class Image(models.Model):
    imagefile = models.ImageField(upload_to='images', )

    # Formats photo before saving
    def save(self, *args, **kwargs):
        if self.imagefile:
            image = Img.open(StringIO.StringIO(self.imagefile.read()))
            image.thumbnail((100,100), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.imagefile= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.imagefile.name, 'image/jpeg', output.len, None)
        super(Image, self).save(*args, **kwargs)


# Event model contains details of each user-created event
class Event(models.Model):
    name = models.CharField(max_length=100)
    starttime = models.DateTimeField('start time', default=datetime.datetime.now())
    endtime = models.DateTimeField('end time', default=datetime.datetime.now())
    location = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, default="")
    reminded = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# Group model contains details of each user-created group
class Group(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField(Event, blank=True)
    def __str__(self):
        return self.name

# Person model contains the details for each user, and contains the events
# and groups that the user belong to
class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, blank=True, null=True)
    profilePicture = models.OneToOneField(Image, blank=True, null=True)

    friends = models.ManyToManyField('self', blank=True, related_name="friends")
    invitedFriends = models.ManyToManyField('self', blank=True, related_name="pendingFriends", symmetrical=False)
    events = models.ManyToManyField(Event, blank=True, related_name="members")
    invitedEvents = models.ManyToManyField(Event, blank=True, related_name="pendingMembers")
    groups = models.ManyToManyField(Group, blank=True)
    receiveReminders = models.BooleanField(default=True)

    def __str__(self):
        return self.name
