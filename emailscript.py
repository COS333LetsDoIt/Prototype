from __future__ import print_function

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'prototype.settings'

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from prototypeApp.models import Person, Group, Event, Image
from django import forms
from django.db import models
from django.forms import ModelForm
#from datetimewidget.widgets import DateTimeWidget
import datetime
from datetime import timedelta
import pytz
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views, authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
# pip install python-dateutil
import dateutil.parser
import re
import json

import prototypeApp.views as views

## imports for photo manipulation ##
from PIL import Image as Img
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import time
import django

django.setup()

interval_minutes = 5
delay            = 60*interval_minutes # delay in seconds
priority_cutoff  = 4


def main():
	# Every "interval" minutes
	while True:
		event_list = Event.objects.all()
		
		for event in event_list:
			if (inSendInterval(event) and (not event.reminded)):
				# Send emails to confirmed participants in the event
				person_list = event.members.all()
				recepient_list = [person.user.email for person in person_list]
				send_mail(event.name + " is in 30 minutes!", 
					event.name + " is in 30 minutes!"            +
						"\nDescription: " + event.description    + 
						"\nLocation: "    + event.location       + 
						"\nTime: "        + str(event.starttime) + " to " + str(event.endtime), 
					'letsdoit.noresponse@gmail.com', recepient_list, fail_silently=True)

				# suggest event to high priority invitees
				person_list = event.pendingMembers.all()
				recepient_list = []
				for person in person_list:
					dictionary = views.calculateScore(person.user, event)
					if dictionary['score'] > priority_cutoff:
						recepient_list.append(person.user.email)

				subj = "Lot's of Friends going to: " + event.name + " in 30 minutes!"
				msg  = ("Lot's of Friends going to: " + event.name + " in 30 minutes!" +
					   "\nDescription: " + event.description      + 
					   "\nLocation: "    + event.location         + 
					   "\nTime: "        + str(event.starttime)   + " to " + str(event.endtime))
				send_mail(subj, msg, 'letsdoit.noresponse@gmail.com', recepient_list, fail_silently=True)


				event.reminded = True
				event.save()

		time.sleep(delay)

def inSendInterval(event):
	low = 30*60
	high = 40*60
	offset = 6*60*60 # since timezones are screwy
	now = datetime.datetime.now()
	now = pytz.utc.localize(now)
	difference = event.starttime - now
	succeed = difference.days == 0 and ((difference.seconds - offset > low) and (difference.seconds - offset < high))
	return succeed

main()

