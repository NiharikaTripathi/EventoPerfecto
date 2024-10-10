from django.shortcuts import render
from .models import Event, Venue, MyClubUser
from datetime import datetime
from calendar import HTMLCalendar
import calendar
import pytz

# Create your views here.
def event_calendar(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    # Convert month name to number
    now = datetime.now()
    tz = pytz.timezone('Asia/Kolkata')
    # localising the objects to the timezone
    now = tz.localize(now)

    month = month.capitalize()
    month_num = list(calendar.month_name).index(month)
    cal = HTMLCalendar().formatmonth(year, month_num)
    time = now.strftime(" %I:%M %p %A %b %d")
    current_year = now.year
    return render(request,
                  "calendar.html",
                  {"month" : month, "year": year, "month_num": month_num,"cal": cal,
                   "time": time,
                   "current_year": current_year} )


def event_details():
    return None


def all_events(request):
    events_list = Event.objects.all()
    return render(request, "event_list.html", {'event_list': events_list})