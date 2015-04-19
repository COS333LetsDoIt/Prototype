from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from prototypeApp.models import Person, Group, Event
from django import forms
from django.db import models
from django.forms import ModelForm
#from datetimewidget.widgets import DateTimeWidget
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views, authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf


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
@login_required()
def index(request):
    event_list = Event.objects.order_by('starttime')
    event_form = get_event_form(request)
    context = {"event_list": event_list, 'form': event_form}
    return render(request, 'prototypeApp/index.html', context)

# Create your views here.
@login_required()
def group(request):
    group_list = Group.objects.order_by('name')
    context = {"group_list": group_list}
    return render(request, 'prototypeApp/group.html', context)

# Create your views here.
@login_required()
def people(request):
    friends_list = Person.objects.order_by('name')
    context = {"friends_list": friends_list}
    return render(request, 'prototypeApp/people.html', context)


def signup(request):
    event_list = Event.objects.order_by('starttime')
    context = {"event_list": event_list}
    return render(request, 'prototypeApp/index.html', context)

@login_required()
def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.person in event.person_set.all():
        user_in_event = True
    else:
        user_in_event = False
    # print event.person_set.all()
    context = {"event": event, "user_in_event": user_in_event}
    return render(request, 'prototypeApp/event.html', context)

# signin page
def login_view(request):
    state = "Please log in:"
    username = ""
    next = request.GET.get('next', "")
    if request.method == "POST":
        #print "POST request received"
        username = request.POST.get('username', '')
        #print "username: " + username
        password = request.POST.get('password', '')
        #print "password: " + password
        user = authenticate(username=username, password=password)
        #print "The user is: " + str(user)
        next = request.POST.get('next', next)
        if user is not None:
            if user.is_active:
                #print "User worked"
                login(request, user)
                #print "Redirecting to next"
                #print "next: " + next
                #print request
                if next == "":
                    return HttpResponseRedirect(reverse('prototypeApp:index'))
                else:
                    return HttpResponseRedirect(next)
            else:
                state = "Please user a nondisabled user:"
                #print "disabled account"
                # Return a 'disabled account' error message
        else:
            # Return an 'invalid login' error message.
            state = "The username or password you entered is incorrect."
    #print "Page outputted"
    context = {'state':state, 'username': username, 'next': next}
    return render(request, 'prototypeApp/login.html', context)    


# new user registration
def register(request):
    state = ""
    username = ""
    email = ""
    password = ""

    if request.method == "POST":
        #print "POST request received"
        username = request.POST.get('username', "")
        #print "username: " + username
        password = request.POST.get('password', "")
        #print "password: " + password
        email = request.POST.get('email', "")
        #print "email: " + email
        
        if User.objects.filter(username=username).exists():
            state = "That user is already taken"
        elif User.objects.filter(email=email).exists():
            state = "That email is already registered"
        else:       
            user = None
            user = User.objects.create_user(username, email, password)
            #### Creates a new person object and links it to the user!
            newPerson = Person()
            newPerson.name = username
            newPerson.user = user
            newPerson.save()
            #print "The user is: " + str(user)
            if user is not None:
                #print "User created"
                user = authenticate(username=username, password=password)

                login(request, user)
                #print "User logged in"
                return HttpResponseRedirect(reverse('prototypeApp:index'))
            else:
                state = "Something is wrong with your input. Try again."
        
    context = {'state':state, 'email': email, 'username': username}
    return render(request, 'prototypeApp/register.html', context)    


# after logging out, return to login
def logout_view(request):
    logout(request)
    #print "User logged off"
    return render(request, 'prototypeApp/login.html', {})

# join event
@login_required()
def join_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     event.person_set.add(request.user.person)
     event.save()
     return HttpResponseRedirect(reverse('prototypeApp:event', args=(event_id,)));

#leave event
@login_required()
def leave_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     event.person_set.remove(request.user.person)
     event.save()
     return HttpResponseRedirect(reverse('prototypeApp:event', args=(event_id,)));
