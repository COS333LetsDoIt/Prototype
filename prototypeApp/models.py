from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from django.shortcuts import render
from django import forms
from django.db import models
from django.forms import ModelForm

#from datetimewidget.widgets import DateTimeWidget
import datetime
from django.http import HttpResponseRedirect

from django.db import models
from django.utils import timezone

from django.forms import ModelForm
from django.forms import ModelForm
from django.contrib.auth.models import User


# imports for photo manipulation ##
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFill

# from django_resized import ResizedImageField
# Create your models here.

#class Event(models.Model):
#   
#




#class Event(models.Model):
#    name = forms.CharField(label='Event name', max_length=100)
 #   starttime = forms.DateTimeField(initial=datetime.datetime.now(), label='Date and Time')
 #   endtime = forms.DateTimeField(initial=datetime.datetime.now(), label='Date and Time')


class Image(models.Model):
    # imagefile = ResizedImageField(max_width=100, max_height=100, upload_to='images')
    imagefile = models.ImageField(upload_to='images', )
    # imageFile = ProcessedImageField(upload_to='images',
    #     processors=[ResizeToFill(100,100)],
    #     format='JPEG',
    #     options={'quality':60})

    # formats photo before saving
    def save(self, *args, **kwargs):
        if self.imagefile:
            image = Img.open(StringIO.StringIO(self.imagefile.read()))
            image.thumbnail((100,100), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.imagefile= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.imagefile.name, 'image/jpeg', output.len, None)
        super(Image, self).save(*args, **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=100)
    starttime = models.DateTimeField('start time', default=datetime.datetime.now())
    endtime = models.DateTimeField('end time', default=datetime.datetime.now())
    location = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField(Event, blank=True)
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, blank=True, null=True)
    #profilePicture = models.URLField(max_length=100, default="http://www.clipartbest.com/cliparts/y4c/9jG/y4c9jGMTE.jpeg") 
    profilePicture = models.OneToOneField(Image, blank=True, null=True) # Many to one relationship
    friends = models.ManyToManyField('self', blank=True, related_name="friends")
    invitedFriends = models.ManyToManyField('self', blank=True, related_name="pendingFriends", symmetrical=False)
    events = models.ManyToManyField(Event, blank=True, related_name="members")
    invitedEvents = models.ManyToManyField(Event, blank=True, related_name="pendingMembers")
    groups = models.ManyToManyField(Group, blank=True)
    
    def __str__(self):
        return self.name
