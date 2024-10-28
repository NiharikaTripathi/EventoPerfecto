from django.urls import path
from . import views


urlpatterns = [
    path('calendar/', views.event_calendar, name='current'),
    path('calendar/<int:year>/<str:month>/', views.event_calendar, name='calendar'),

    path('list_venues/', views.all_venues, name='list-venues'),
    path('show_venue/<int:venue_id>', views.show_venue, name='show-venue'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('search_venue/', views.search_venue, name='search-venue'),
    path('update_venue/<int:venue_id>', views.update_venue, name='update-venue'),
    path('delete_venue/<int:venue_id>', views.delete_venue, name='delete-venue'),

    path('venue_text/', views.venue_text, name='venue-text'),
    path('venue_csv/', views.venue_csv, name='venue-csv'),
    path('venue_pdf/', views.venue_pdf, name='venue-pdf'),
    path('event_text/', views.event_text, name='event-text'),
    path('event_csv/', views.event_csv, name='event-csv'),
    path('event_pdf/', views.event_pdf, name='event-pdf'),

    path('list_events/', views.all_events, name='list-events'),
    path('add_event/', views.add_event, name='add-event'),
    path('update_event/<int:event_id>', views.update_event, name='update-event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete-event'),
    path('my_events/', views.my_events, name='my-events'),
    path('search_events/', views.search_events, name='search-events'),

]

