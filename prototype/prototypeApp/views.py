from django.shortcuts import render
from prototypeApp.models import Person, Group, Event

# Create your views here.
def index(request):
	context = {}
	return render(request, 'prototypeApp/index.html',context)
