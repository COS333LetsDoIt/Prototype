from django.shortcuts import render
from django import forms
from django.db import models
from django.forms import ModelForm

#from datetimewidget.widgets import DateTimeWidget
import datetime
from django.http import HttpResponseRedirect


import datetime
from django.db import models
from django.utils import timezone

from django.forms import ModelForm

# Create your models here.

#class Event(models.Model):
#   
#

from django.forms import ModelForm


#class Event(models.Model):
#    name = forms.CharField(label='Event name', max_length=100)
 #   starttime = forms.DateTimeField(initial=datetime.datetime.now(), label='Date and Time')
 #   endtime = forms.DateTimeField(initial=datetime.datetime.now(), label='Date and Time')


class Event(models.Model):
    name = models.CharField(max_length=100)
    starttime = models.DateTimeField('start time')
    endtime = models.DateTimeField('end time')
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField(Event, blank=True)
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    friends = models.ManyToManyField('self', blank=True)
    events = models.ManyToManyField(Event, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.name






