from django.contrib import admin
from prototypeApp.models import Event, Person, Group

class PersonInlineForEvents(admin.TabularInline):
	model = Person.events.through

class GroupInlineForEvents(admin.TabularInline):
	model = Group.events.through

class PersonInlineForGroups(admin.TabularInline):
	model = Person.groups.through

class EventAdmin(admin.ModelAdmin):
	inlines = [PersonInlineForEvents, GroupInlineForEvents]

class GroupAdmin(admin.ModelAdmin):
	inlines = [PersonInlineForGroups]

# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Person)
