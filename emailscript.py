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
delay = 60*interval_minutes #60 seconds


def main():
	# Every "interval" minutes
	while True:
		event_list = Event.objects.all()
		
		for event in event_list:
			print(event.name)
			if (inSendInterval(event) and (not event.reminded)):
				print("sending emails!")
				person_list = event.members.all()
				recepient_list = [person.user.email for person in person_list]
				send_mail(event.name + " is in 30 minutes!", 
					event.name + " is in 30 minutes!"            +
						"\nDescription: " + event.description    + 
						"\nLocation: "    + event.location       + 
						"\nTime: "        + str(event.starttime) + " to " + str(event.endtime), 
					"no_response@letsdoit.com",
					recepient_list, fail_silently=True)
				event.reminded = True
				event.save()

		time.sleep(delay)

def inSendInterval(event):
	low = 10*60
	high = 400*60
	offset = 6*60*60 # since timezones are screwy
	now = datetime.datetime.now()
	now = pytz.utc.localize(now)
	difference = event.starttime - now
	print("Now: ") 
	print(now)
	print("Start: ")
	print(event.starttime)
	print("Difference in hours: ")
	print((0.0+difference.seconds - offset)/60/60)
	succeed = difference.days == 0 and ((difference.seconds - offset > low) and (difference.seconds - offset < high))
	print("Succeeded?: ")
	print(succeed)
	return succeed

main()

