from django.contrib import admin
from .models import MyClubUser, Event, Venue

# Register your models here.
admin.site.register(MyClubUser)
admin.site.register(Event)
admin.site.register(Venue)