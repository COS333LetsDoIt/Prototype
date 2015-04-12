from django.shortcuts import render
from prototypeApp.models import Person, Group, Event
from django import forms
from django.db import models
from django.forms import ModelForm
#from datetimewidget.widgets import DateTimeWidget
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
@login_required(login_url='prototypeApp/login/')
def index(request):
    event_list = Event.objects.order_by('starttime')
    event_form = get_event_form(request)
    context = {"event_list": event_list, 'form': event_form}
    return render(request, 'prototypeApp/index.html', context)

# Create your views here.
def group(request):
    group_list = Group.objects.order_by('name')
    context = {"group_list": group_list}
    return render(request, 'prototypeApp/group.html', context)


def signup(request):
    event_list = Event.objects.order_by('starttime')
    context = {"event_list": event_list}
    return render(request, 'prototypeApp/index.html', context)

# signin page
def login(request):
    context = {}
    return render(request, 'prototypeApp/signin.html', context)    
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(username=username, password=password)
    # context = {}

    # if user is not None and user.is_active:
    #     login(request, user)
    # else:
    #     return render(request, 'prototypeApp/sigin_error.html', context)
