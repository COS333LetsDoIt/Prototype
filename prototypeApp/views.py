from __future__ import print_function
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
# pip install python-dateutil
import dateutil.parser
import re
import json


################################################################################
# Forms 
################################################################################

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'description']

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

# taken from https://docs.djangoproject.com/en/1.8/topics/forms/#forms-in-django
def get_event_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST)
        # check whether it's valid:
        # print request.POST
        print (form.is_valid())
        print (form.errors)
        print (request.POST)
        starttime = request.POST.get("starttime", None)
        endtime = request.POST.get("endtime", None)
            
        if form.is_valid() and starttime and endtime:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # new_event = form.save()
            #print "hi"
            #print request.POST.get("friends", '').split(', ')
            # for friend_name in request.POST.get("friends", '').split(', '):
            #     friends = Person.objects.filter(name=friend_name)
            #     #print "found friend"
            #     new_event.members.add(request.user.person)
            #     if friends.exists():
            #         new_event.pendingMembers.add(friends[0])
            #         #friends[0].event_set.add(new_event)
            #         #print "added friend to event"


            starttime = dateutil.parser.parse(starttime)
            endtime = dateutil.parser.parse(endtime)

            if starttime < endtime:
                new_event = form.save()

                new_event.starttime = starttime
                new_event.endtime = endtime

                # add friends to events
                for friend_name in request.POST.get("friends", '').split(', '):
                    friends = Person.objects.filter(name=friend_name)
                    #print "found friend"
                    new_event.members.add(request.user.person)
                    if friends.exists() and friends[0] not in new_event.members.all():
                        invite_event(new_event, friends[0])
                        #friends[0].event_set.add(new_event)
                        #print "added friend to event"



                # add groups to events
                for group_name in request.POST.get("groups", '').split(','):
                    groups = Group.objects.filter(name=group_name) # what if there is multiple groups with same name?
                    
                    if groups.exists():
                        group = groups[0]
                        for person in group.person_set.all():
                            if person.id != request.user.person.id and person not in new_event.pendingMembers.all():
                                invite_event(new_event, person)

                new_event.save()

    # if a GET (or any other method) we'll create a blank form
    
    form = EventForm(initial={'starttime': datetime.datetime.now(), 'endtime': datetime.datetime.now()})
    return form

# taken from https://docs.djangoproject.com/en/1.8/topics/forms/#forms-in-django
def get_group_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GroupForm(request.POST)
        # check whether it's valid:
        #print (request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_group = form.save()

            # add friends to groups
            for friend_name in request.POST.get("friends", '').split(', '):
                friends = Person.objects.filter(name=friend_name)
                #print "found friend"
                new_group.person_set.add(request.user.person)
                if friends.exists():
                    new_group.person_set.add(friends[0])

    # if a GET (or any other method) we'll create a blank form
    
    form = GroupForm()
    return form

################################################################################
# Index page
################################################################################

@login_required()
def index(request):
    event_list = request.user.person.events.all()
    invited_event_list = request.user.person.invitedEvents.all()

    # works out events of friends of friends
    friend_set = request.user.person.friends.all()
    friend_event_list = set()
    for friend in friend_set:
        friend_events = friend.events.all();
        for event in friend_events:
            if event not in event_list and event not in invited_event_list:
                friend_event_list.add(event)

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())


    event_form = get_event_form(request)
    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in request.user.person.friends.all()])
    groups_list = json.dumps([{"label": group.name, "id": group.id, "value": group.name} for group in request.user.person.groups.all()])
    
    context = {"event_list": event_list, 
    'groups_list': groups_list, 
    'invited_event_list': invited_event_list, 
    'friend_event_list': friend_event_list, 
    'form': event_form, 
    'friends_list': friends_list,
    'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}

    return render(request, 'prototypeApp/index.html', context)

################################################################################
# Events
################################################################################

@login_required()
def event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.person in event.members.all():
        user_in_event = True
    else:
        user_in_event = False

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    # print event.person_set.all()
    context = {"event": event, "user_in_event": user_in_event, 'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}
    return render(request, 'prototypeApp/event.html', context)

# join event
@login_required()
def join_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     event.members.add(request.user.person)
     event.pendingMembers.remove(request.user.person)
     event.save()
     return HttpResponseRedirect(reverse('prototypeApp:event', args=(event_id,)));

@login_required()
def decline_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     event.pendingMembers.remove(request.user.person)
     event.save()
     return HttpResponseRedirect(reverse('prototypeApp:index'));

def invite_event(event, person):
     if person not in event.members.all():
        event.pendingMembers.add(person)
        event.save()

@login_required()
def leave_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     event.members.remove(request.user.person)
     event.save()
     return HttpResponseRedirect(reverse('prototypeApp:event', args=(event_id,)))



################################################################################
# Groups
################################################################################

@login_required()
def group(request):
    group_list = request.user.person.groups.all()
    group_form = get_group_form(request)

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    source = []

    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in request.user.person.friends.all()])
    context = {"group_list": group_list,
    'form': group_form,
    "friends_list": friends_list,
    'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}
    return render(request, 'prototypeApp/group.html', context)

@login_required()
def aGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    # add friend to existing group
    if request.method == 'POST':
        for friend_name in request.POST.get("friends", '').split(', '):
            friends = Person.objects.filter(name=friend_name)
            #print "found friend"
            if friends.exists():
                group.person_set.add(friends[0])

    if request.user.person in group.person_set.all():
        user_in_group = True
    else:
        user_in_group = False
    # print event.person_set.all()

    # get list of friends who are not in group yet
    friends = request.user.person.friends.all()
    friends = friends.exclude(id__in=group.person_set.all())
    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in friends])

    context = {"group": group, "user_in_group": user_in_group, "friends_list": friends_list,'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}
    return render(request, 'prototypeApp/aGroup.html', context)

@login_required()
def leave_group(request, group_id):
     group = get_object_or_404(Group, pk=group_id)
     group.person_set.remove(request.user.person)
     group.save()

     if len(group.person_set.all()) == 0:
        group.delete()
        return HttpResponseRedirect(reverse('prototypeApp:group'))
     else:
        return HttpResponseRedirect(reverse('prototypeApp:group'))

     return HttpResponseRedirect(reverse('prototypeApp:aGroup', args=(group_id,)))



################################################################################
# Friends
################################################################################

# Create your views here.
@login_required()
def people(request):
    #friends_list = Person.objects.order_by('name')
    if request.method == 'POST':
        for friend_name in request.POST.get("friends", '').split(', '):
            friends = Person.objects.filter(name=friend_name)
            #print "found friend"
            if friends.exists():
                add_friend(request, friends[0].id)

    people = Person.objects.exclude(id=request.user.person.id)
    people = people.exclude(id__in=request.user.person.friends.all())
    people = people.exclude(id__in=request.user.person.invitedFriends.all())
    people = people.exclude(id__in=request.user.person.pendingFriends.all())

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    people_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in people])
    friends_list = request.user.person.friends.all()
    pending_friends_list = request.user.person.pendingFriends.all()
    invited_friends_list = request.user.person.invitedFriends.all()
    context = {
        "friends_list": friends_list, 
        "people_list": people_list, 
        "pending_friends_list": pending_friends_list,
        "invited_friends_list": invited_friends_list,
        "pending_friend_count": pending_friend_count,
        "pending_event_count": pending_event_count
    }
    return render(request, 'prototypeApp/people.html', context)

def add_friend(request, friend_id):
    friend = get_object_or_404(Person, pk=friend_id)
    if request.user.person in friend.invitedFriends.all():
        request.user.person.friends.add(friend)
        request.user.person.pendingFriends.remove(friend)
    else:
        request.user.person.invitedFriends.add(friend)
    return HttpResponseRedirect(reverse('prototypeApp:people'));

def decline_friend(request, friend_id):
    friend = get_object_or_404(Person, pk=friend_id)
    if request.user.person in friend.invitedFriends.all():
        request.user.person.pendingFriends.remove(friend)
        
    return HttpResponseRedirect(reverse('prototypeApp:people'));

def remove_friend(request, friend_id):
    friend = get_object_or_404(Person, pk=friend_id)
    request.user.person.friends.remove(friend)
    return HttpResponseRedirect(reverse('prototypeApp:people'));




################################################################################
# User oprations (Sign-in / Register / Change user profile)
################################################################################

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


def profile(request):
    user = request.user;
    context = {"user": user}
    return render(request, 'prototypeApp/profile.html', context)


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
        # elif re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) == None:
        #         state = "That email address is not valid"
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
                return HttpResponseRedirect(reverse('prototypeApp:people'))
            else:
                state = "Something is wrong with your input. Try again."
        
    context = {'state':state, 'email': email, 'username': username}
    return render(request, 'prototypeApp/register.html', context)    

# after logging out, return to login
def logout_view(request):
    logout(request)
    #print "User logged off"
    return render(request, 'prototypeApp/login.html', {})


# What what is this??
# def signup(request):
#     event_list = Event.objects.order_by('starttime')
#     context = {"event_list": event_list}
#     return render(request, 'prototypeApp/index.html', context)




# def sdk(request):
#     context = {}
#     return render(request, 'prototypeApp/sdk.html', context)
