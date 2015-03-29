import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

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






