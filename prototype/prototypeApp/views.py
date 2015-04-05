from django.shortcuts import render
from prototypeApp.models import Person, Group, Event

# Create your views here.
def index(request):
	event_list = Event.objects.order_by('starttime')
	context = {"event_list": event_list}
	return render(request, 'prototypeApp/index.html', context)
