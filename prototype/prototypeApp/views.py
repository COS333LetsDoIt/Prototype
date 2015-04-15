from django.shortcuts import render, get_object_or_404
from prototypeApp.models import Person, Group, Event
from django import forms
from django.db import models
from django.forms import ModelForm

#from datetimewidget.widgets import DateTimeWidget
import datetime
from django.http import HttpResponseRedirect


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name','starttime','endtime']


#starttime
#endtime
#friends
#groups

# taken from https://docs.djangoproject.com/en/1.8/topics/forms/#forms-in-django
def get_event_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_event = form.save()
    # if a GET (or any other method) we'll create a blank form
    
    form = EventForm(initial={'starttime': datetime.datetime.now(), 'endtime': datetime.datetime.now()})

    return form

# Create your views here.
def index(request):
    event_list = Event.objects.order_by('starttime')
    event_form = get_event_form(request)
    context = {"event_list": event_list, 'form': event_form}
    return render(request, 'prototypeApp/index.html', context)

def signup(request):
    event_list = Event.objects.order_by('starttime')
    context = {"event_list": event_list}
    return render(request, 'prototypeApp/index.html', context)

def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    print event.person_set.all()
    context = {"event": event}
    return render(request, 'prototypeApp/event.html', context)