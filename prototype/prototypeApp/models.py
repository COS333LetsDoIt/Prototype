import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
	name = models.CharField(max_length=100)
	friends = models.ManyToManyField('self')
	events = models.ManyToManyField(Event)
	groups = models.ManyToManyField(Group)


class Group(models.Model):
	name = models.CharField(max_length=100)
	events = models.ManyToManyField(Event)

class Event(models.Model):
	name = models.CharField(max_length=100)
	starttime = models.DateTimeField('start time')
	endtime = models.DateTimeField('end time')

