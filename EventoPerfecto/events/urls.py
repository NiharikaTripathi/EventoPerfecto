from django.urls import path
from . import views
urlpatterns = [
    path('list_events', views.all_events, name='list-events'),
    path('calendar/', views.event_calendar, name='current'),
    path('calendar/<int:year>/<str:month>/', views.event_calendar, name='calendar'),
    path('event-details/<str:id>/', views.event_details, name='event-details'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('list_venues/', views.all_venues, name='list-venue'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
]