from django.urls import path
from . import views
urlpatterns = [
    path('', views.all_events, name='list-events'),
    path('calendar/', views.event_calendar, name='current'),
    path('calendar/<int:year>/<str:month>/', views.event_calendar, name='calendar'),
    path('event-details/<str:id>/', views.event_details, name='event-details'),
]