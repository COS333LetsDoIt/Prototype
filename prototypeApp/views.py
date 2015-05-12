################################################################################
# views.py
# Contains functions that handle the interaction between the user input and the
# database, and returns the page to be displayed to the user.
################################################################################

from __future__ import print_function

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views, authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.files.uploadedfile import InMemoryUploadedFile

from prototypeApp.models import Person, Group, Event, Image
import dateutil.parser
import re
import json
import datetime
from datetime import timedelta
import pytz

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

class ImageForm(forms.Form):
    imagefile = forms.ImageField(
        label='Select a file',
    )

##############################################################################

# Function to handle profile picture uploads from an image form
def create_image_from_form(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        newImage = Image(imagefile = request.FILES['imagefile'])
        newImage.save()
        request.user.person.profilePicture = newImage
        request.user.person.save()
    form = ImageForm()
    return form

##############################################################################

# Function to create an event from an event form. Adapted from
# https://docs.djangoproject.com/en/1.8/topics/forms/#forms-in-django
def create_event_from_form(request):

    # Create a form instance and populate it with data from the request:
    form = EventForm(request.POST)

    starttime = request.POST.get("starttime", None)
    endtime = request.POST.get("endtime", None)

    # Checks whether the form is valid, and if the starttime given is earlier
    # than the endtime of the event
    if form.is_valid() and starttime and endtime:
        starttime = dateutil.parser.parse(starttime)
        endtime = dateutil.parser.parse(endtime)

        if starttime < endtime:
            new_event = form.save()

            new_event.starttime = starttime
            new_event.endtime = endtime
            new_event.reminded = False

            # Add friends to events
            for friend_name in request.POST.get("friends", '').split(', '):
                friends = Person.objects.filter(name=friend_name)
                new_event.members.add(request.user.person)
                if friends.exists() and friends[0] not in new_event.members.all():
                    invite_event(new_event, friends[0])

            # Add Groups to events
            for group_name in request.POST.get("groups", '').split(','):
                groups = Group.objects.filter(name=group_name)

                if groups.exists():
                    group = groups[0]
                    for person in group.person_set.all():
                        if person.id != request.user.person.id and person not in new_event.pendingMembers.all():
                            invite_event(new_event, person)

            new_event.save()
            return "Success"

        else: # starttime > endtime, should not allow the user to create such event
            return None
    return None

##############################################################################

# Function to create a group from a group form.
def create_group_from_form(request):
    # Create a form instance and populate it with data from the request:
    form = GroupForm(request.POST)

    # Check whether form submitted is valid:
    if form.is_valid():

        # Creates new group if the form is valid
        new_group = form.save()

        # Add friends to groups
        for friend_name in request.POST.get("friends", '').split(', '):
            friends = Person.objects.filter(name=friend_name)
            new_group.person_set.add(request.user.person)
            if friends.exists():
                new_group.person_set.add(friends[0])

################################################################################
# Functions for Index page
################################################################################

# Calculates the relevance score for an event to a user. The relevance score
# is (number of friends attending to event + 0.5* number of friends invited).
# Events that have already ended get a negative relevance score.
def calculateScore(user, event):
    # Calculates the number of friends attending and invited to an event
    people_in_event     = 0;
    friends_in_event    = 0;
    friends_invited     = 0;
    score               = 0.0;

    for person in event.members.all():
        people_in_event += 1.0;
        if person in user.person.friends.all():
            score += 1.0
            friends_in_event += 1

    for person in event.pendingMembers.all():
        people_in_event += 1.0;
        if person in user.person.friends.all():
            score += 0.5
            friends_invited += 1

    # Negative relevance score for events that have already ended
    now = datetime.datetime.now()
    now = pytz.utc.localize(now)
    now += timedelta(hours=6)

    diffStart = event.starttime - now
    diffEnd   = event.endtime - now

    if diffEnd.total_seconds() < 0:
        score = -1.0

    return {'score': score,
    'friends_in_event': friends_in_event,
    'friends_invited': friends_invited}

##############################################################################

# Each EventScore object contains a event and its corresponding relevance score,
# as well as the number of friends attending and invited to an event. This
# facilitates sorting events based on relevance.
class EventStats:
    def __init__(self, user, event):
        self.event              = event;
        eventScore              = calculateScore(user, event)
        self.score              = eventScore['score']
        self.friends_in_event   = eventScore['friends_in_event']
        self.friends_invited    = eventScore['friends_invited']
        self.formattedTime      = getFormattedTime(event)

    def __str__(self):
        return self.event.name + ":" + str(self.score)

##############################################################################

# Sorts list of events based on the relevance
def sortEventsByRelevance(user, event_list):
    allEventStats = []
    for event in event_list:
        allEventStats.append(EventStats(user, event))

    allEventStats = sorted(allEventStats, key=lambda eventstats:eventstats.score, reverse=True)
    return allEventStats

##############################################################################

# Sorts list of events based on the starttime
def sortEventsByTime(user, event_list):
    futureEvents = []
    pastEvents = []
    cutoff = datetime.datetime.now()
    cutoff = pytz.utc.localize(cutoff) + timedelta(hours=6)

    for event in event_list:
        if event.endtime < cutoff:
            pastEvents.append(EventStats(user,event))
        else:
            futureEvents.append(EventStats(user,event))

    pastEvents = sorted(pastEvents, key=lambda eventstats:eventstats.event.starttime, reverse=True)
    futureEvents = sorted(futureEvents, key=lambda eventstats:eventstats.event.starttime, reverse=False)

    futureEvents.extend(pastEvents)
    return futureEvents

##############################################################################

# Helper function to determine if an event is over and should be allowed 
#to be joined.

def isEventOver(event):
    now = datetime.datetime.now()
    now = pytz.utc.localize(now)
    now += timedelta(hours=6)

    diffStart = event.starttime - now
    diffEnd   = event.endtime - now

    return (diffEnd.total_seconds() < 0)

# Helper function to format the time for each event, such as "In 15 minutes"
# or "Tomorrow at 13:00"
def getFormattedTime(event):
    now = datetime.datetime.now()
    now = pytz.utc.localize(now)
    now += timedelta(hours=6)

    diffStart = event.starttime - now
    diffEnd   = event.endtime - now

    if diffEnd.total_seconds() < 0:
        return "Event over"

    elif diffStart.total_seconds() < 0:
        return "Happening now"

    # Events less than one hour away
    elif diffStart.total_seconds() < 3600:
        minutes = int(diffStart.total_seconds() / 60)

        if minutes == 0:
            return "Happening now"
        if minutes == 1:
            return "In " + str(minutes) + " minute"
        else:
            return "In " + str(minutes) + " minutes"

    # Events less than 3 hours away
    elif diffStart.total_seconds() < (3600*3):
        hours = int (round(diffStart.total_seconds() / 3600))
        if hours == 1:
            return "In " + str(hours) + " hour"
        else:
            return "In " + str(hours) + " hours"

    # Events starting today
    elif event.starttime.day == now.day and event.starttime.year == now.year:
        return "Today at " + str( (event.starttime - timedelta(hours=5)).time().strftime("%I:%M %p"))

    # Events starting tomorrow
    elif event.starttime.day == now.day + 1 and event.starttime.year == now.year:
        return "Tomorrow at " + str( (event.starttime - timedelta(hours=5)).time().strftime("%I:%M %p"))

    else:
        return event.starttime

##############################################################################

# Deletes old events  (which have ended more than 2 days ago)
def full_event_cleanup():
    cutoff = datetime.datetime.now()
    delta = timedelta(days=2)
    cutoff = cutoff - delta
    cutoff = pytz.utc.localize(cutoff)

    for event in Event.objects.all():
        current = event.endtime

        if (current <= cutoff):
            event.delete()

##############################################################################

# View for index page, with events sorted by start time
@login_required()
def indexByTime(request):
    return index(request, False)

##############################################################################

# View for index page
@login_required()
def index(request, sortByRelevance=True):

    # Gets rid of old events globally
    full_event_cleanup()

    # Sorts events
    if sortByRelevance:
        event_list = sortEventsByRelevance(request.user, request.user.person.events.all())
        invited_event_list = sortEventsByRelevance(request.user, request.user.person.invitedEvents.all())
    else:
        event_list = sortEventsByTime(request.user, request.user.person.events.all())
        invited_event_list = sortEventsByTime(request.user, request.user.person.invitedEvents.all())


    # Works out events of friends of friends, and sorts based on either relevance or
    # start time
    friend_set = request.user.person.friends.all()
    friend_event_list = set()
    for friend in friend_set:
        friend_events = friend.events.all();
        for event in friend_events:
            if event not in event_list and event not in invited_event_list:
                friend_event_list.add(event)

    if sortByRelevance:
        friend_event_list = sortEventsByRelevance(request.user, friend_event_list)
    else:
        friend_event_list = sortEventsByTime(request.user, friend_event_list)

    # Counts number of pending event and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    # Error message if the user attempts to create an event where the start time
    # is earlier than the end time
    state = ""
    if request.method == 'POST':
        success_msg = create_event_from_form(request)
        event_form = EventForm(request.POST)
        if success_msg == None:
            # starttime > endtime
            state = "Event start time is later than the end time!"
            friends_list = None
            groups_list = None
        else:
            return HttpResponseRedirect('')
    else:
        event_form = EventForm(initial={'starttime': datetime.datetime.now(), 'endtime': datetime.datetime.now()})

    # Generates json of user's friends and groups for the create event form
    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in request.user.person.friends.all()])
    groups_list = json.dumps([{"label": group.name, "id": group.id, "value": group.name} for group in request.user.person.groups.all()])

    # Renders the webpage
    context = {"event_list": event_list,
    'groups_list': groups_list,
    'invited_event_list': invited_event_list,
    'friend_event_list': friend_event_list,
    'form': event_form,
    'friends_list': friends_list,
    'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count,
    'state': state,
    'sortByRelevance': sortByRelevance}

    return render(request, 'prototypeApp/index.html', context)


################################################################################
# Functions for Event Page
################################################################################

# View for the event page
@login_required()
def event(request, event_id):

    event = get_object_or_404(Event, pk=event_id)

    event_list = request.user.person.events.all()
    invited_event_list = request.user.person.invitedEvents.all()

    # counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    # works out events of friends of friends
    friend_set = request.user.person.friends.all()
    friend_event_list = set()
    for friend in friend_set:
        friend_events = friend.events.all();
        for currEvent in friend_events:
            if currEvent not in event_list and currEvent not in invited_event_list:
                friend_event_list.add(event)


    if request.user.person in event.members.all():
        user_in_event = True
    elif request.user.person in event.pendingMembers.all() or event in friend_event_list:
        user_in_event = False
    else:
        context = {"item": "event", 'pending_event_count': pending_event_count, 'pending_friend_count': pending_friend_count}
        return render(request, 'prototypeApp/forbidden.html', context)


    # print event.person_set.all()
    context = {
        "event": event, 
        "user_in_event": user_in_event, 
        "pending_event_count": pending_event_count, 
        "event_over": isEventOver(event),
        'pending_friend_count': pending_friend_count
    }
    return render(request, 'prototypeApp/event.html', context)

##############################################################################

# Functions that allow use to join an event, decline an event, invite
# a friend to an event and leave an event
@login_required()
def join_event(request, event_id):
     event = get_object_or_404(Event, pk=event_id)
     if (not isEventOver(event)):
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
     if (not isEventOver(event)):
         event.members.remove(request.user.person)
         event.save()
     return HttpResponseRedirect(reverse('prototypeApp:index'));



################################################################################
# Groups
################################################################################


# View for the groups page, listing all the groups that the user belongs to
@login_required()
def group(request):
    group_list = request.user.person.groups.all()
    if request.method == 'POST':
        create_group_from_form(request)
        return HttpResponseRedirect('')
    else:
        group_form = GroupForm()

    # Counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())


    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in request.user.person.friends.all()])

    context = {"group_list": group_list,
    'form': group_form,
    "friends_list": friends_list,
    'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}
    return render(request, 'prototypeApp/group.html', context)

##############################################################################

# View for the individual group page, listing the details of a particular
# group
@login_required()
def aGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    # Counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())


    # Add friend to existing group
    if request.method == 'POST':
        for friend_name in request.POST.get("friends", '').split(', '):
            friends = Person.objects.filter(name=friend_name)
            if friends.exists():
                group.person_set.add(friends[0])

    if request.user.person in group.person_set.all():
        user_in_group = True
    else:
        context = {"item": "group", 'pending_event_count': pending_event_count, 'pending_friend_count': pending_friend_count}
        return render(request, 'prototypeApp/forbidden.html', context)


    # Get list of friends who are not in group yet
    friends = request.user.person.friends.all()
    friends = friends.exclude(id__in=group.person_set.all())
    friends_list = json.dumps([{"label": friend.name, "id": friend.id, "value": friend.name} for friend in friends])

    context = {"group": group, "user_in_group": user_in_group, "friends_list": friends_list,'pending_event_count': pending_event_count,
    'pending_friend_count': pending_friend_count}
    return render(request, 'prototypeApp/aGroup.html', context)

##############################################################################

# Function that allow user to leave a group
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
# Functions for Friends page
################################################################################

# Veiw for friends page
@login_required()
def people(request):

    # Adds friends to user from a form
    if request.method == 'POST':
        for friend_name in request.POST.get("friends", '').split(', '):
            friends = Person.objects.filter(name=friend_name)
            if friends.exists():
                add_friend(request, friends[0].id)

    # Generates list of other users that a user can befriend
    people = Person.objects.exclude(id=request.user.person.id)
    people = people.exclude(id__in=request.user.person.friends.all())
    people = people.exclude(id__in=request.user.person.invitedFriends.all())
    people = people.exclude(id__in=request.user.person.pendingFriends.all())

    # Counts number of pending events and friend invites
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

##############################################################################

# Functions that allow user to add friend, remove friend and decline a friend
# request
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

# Signin page
def login_view(request):
    state = "Please log in:"
    username = ""
    next = request.GET.get('next', "")
    if request.method == "POST":

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        next = request.POST.get('next', next)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.has_key('remember_me'):
                    request.session.set_expiry(1209600) # 2 weeks
                if next == "":
                    return HttpResponseRedirect(reverse('prototypeApp:index'))
                else:
                    return HttpResponseRedirect(next)
            else:
                state = "Please use a nondisabled user:"
        else:
            # Return an 'invalid login' error message.
            state = "The username or password you entered is incorrect."
    context = {'state':state, 'username': username, 'next': next}
    return render(request, 'prototypeApp/login.html', context)

##############################################################################

# Profile page
@login_required()

def profile(request):
    user = request.user;

    # Lets user change whether they want to receive email reminders
    if request.method == "POST" and request.POST.has_key('receiving'):
        user.person.receiveReminders = request.POST.has_key('receive_reminders')
        user.person.save()

    receive_reminders = user.person.receiveReminders

    # Counts number of pending events and friend invites
    pending_event_count = len(request.user.person.invitedEvents.all())
    pending_friend_count = len(request.user.person.pendingFriends.all())

    # Lets user change change their profile picture
    if request.method == 'POST':
        create_image_from_form(request)
        return HttpResponseRedirect('')
    else:
        image_form = ImageForm()

    context = {
        "user": user,
        "form": image_form,
        "pending_event_count": pending_event_count,
        "pending_friend_count": pending_friend_count,
        "receive_reminders": receive_reminders
    }
    return render(request, 'prototypeApp/profile.html', context)

##############################################################################

# New user registration
def register(request):
    state = ""
    username = ""
    email = ""
    password = ""

    if request.method == "POST":
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        email = request.POST.get('email', "")

        if User.objects.filter(username=username).exists():
            state = "That name is already taken. Please add a middlename or epithet."
        elif User.objects.filter(email=email).exists():
            state = "That email is already registered."
        else:
            user = None
            user = User.objects.create_user(username, email, password)

            # Creates a new person object and links it to the user
            newPerson = Person()
            newPerson.name = username
            newPerson.user = user
            newPerson.save()

            if user is not None:
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('prototypeApp:about'))
            else:
                state = "Something is wrong with your input. Try again."

    context = {'state':state, 'email': email, 'username': username}
    return render(request, 'prototypeApp/register.html', context)

# After logging out, return to login
def logout_view(request):
    logout(request)
    #print "User logged off"
    return render(request, 'prototypeApp/login.html', {})


################################################################################
# About page
################################################################################

def about(request):
    user = request.user
    if user.is_anonymous():
        context = {
        "user": user,
        }
    else:
        pending_event_count = len(request.user.person.invitedEvents.all())
        pending_friend_count = len(request.user.person.pendingFriends.all())
        context = {
        "user": user,
        "pending_event_count": pending_event_count,
        "pending_friend_count": pending_friend_count,
        }
    return render(request, 'prototypeApp/about.html', context)
