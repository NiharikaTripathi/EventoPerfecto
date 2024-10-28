from django.contrib import admin
from .models import Event, Venue

# Register your models here.
# admin.site.register(MyClubUser)
# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    # list_display changes the things on the main page
    list_display = ('name', 'address', 'phone', 'email')
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventModel(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)