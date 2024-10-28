from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from calendar import HTMLCalendar
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import csv
import calendar
import io

from .forms import VenueForm, EventForm, EventFormAdmin
from .models import Event, Venue

# View to display Calendar
def event_calendar(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    now = datetime.now()
    month_num = list(calendar.month_name).index(month.capitalize()) # Convert month name to number
    month_num = int(month_num)
    cal = HTMLCalendar().formatmonth(year, month_num)
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_num
    )
    time = now.strftime(" %I:%M %p %A %b %d")
    current_year = now.year
    return render(request, "calendar.html",
                  {"month" : month, "year": year, "month_num": month_num,"cal": cal,
                   "time": time,
                   "current_year": current_year,
                   "event_list":event_list} )


#Event Views
# Display all Events
def all_events(request):
    events_list = Event.objects.all().order_by('event_date')
    return render(request, "event_list.html", {'event_list': events_list})


# Add an Event
def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_event.html',{'form' :form, 'submitted': submitted})


# Update an Event
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser or request.user == event.manager:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            return redirect('list-events')
    return render(request, "update_event.html", {'event': event, 'form': form})


# Delete an Event
def delete_event(request, event_id):
    try :
        print("\n here")
        event = Event.objects.get(pk=event_id)
        name = event.name
        if request.user == event.manager:
            print("\n here 3")
            event.delete()
            messages.success(request, ("The venue has been successfully deleted!!"))
            return redirect('list-events')
        else:
            messages.success(request, (f"You aren't Authorized To Delete This Event - {name}!!"))
            return redirect('list-events')
    except Exception as e:
        messages.success(request, (f"Error: {e}. No such event exists with id {event_id}!!"))
        return redirect('list-events')

# Show my events
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        event_list = Event.objects.filter(Q(manager=me) | Q(attendees=me))
        # event_list = Event.objects.filter(attendees = me)
        return render(request, "my_events.html", {'event_list':event_list})
    else:
        messages.success(request, "You are not authorized to view this page.")
        return redirect('homepage')


# Search event
def search_events(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        event_list = Event.objects.filter(description__contains=searched)
        return render(request, "search_event.html", {'searched':searched, 'event_list':event_list})
    else :
        return render(request, "search_event.html", {})


# Venue Views
# Add a Venue
def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/event_app/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_venue.html',{'form' :form, 'submitted': submitted})


# Display all Venues list
def all_venues(request):
    p=Paginator(Venue.objects.all(), 4) # Set up pagination: Paginator(call_to_db, per_page)
    page = request.GET.get('page')
    venues = p.get_page(page)
    # venue_list = Venue.objects.all().order_by("?") # To show data in random order
    nums = "a" * venues.paginator.num_pages
    return render(request, "venues.html", {'venues': venues, 'nums':nums})


# Display details of a Venue
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, "show_venue.html",
                  {'venue': venue,
                   'venue_owner':venue_owner.first_name + " " + venue_owner.last_name})


# Search Venue by name
def search_venue(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, "search_venue.html", {'searched':searched, 'venues': venues})
    else:
        return render(request, "search_venue.html", {})


# Update a Venue
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if venue.owner == request.user.id:
        if form.is_valid():
            form.save()
            return redirect('list-venues')
        return render(request, "update_venue.html", {'venue' : venue, 'form':form})
    else:
        messages.success(request, "You are not authorized to update this venue. Only owner and admin can update.")


# Delete a Venue
def delete_venue(request, venue_id):
        venue = Venue.objects.get(pk=venue_id)
        if venue.owner == request.user.id:
            venue.delete()
            messages.success(request, ("The venue has been successfully deleted!!"))
            return redirect('list-venues')
        else:
            messages.success(request, ("You can't delete the venue!!"))
            return redirect('list-venues')





# Downloading file in different format
# Generating text file containing all venues dynamically
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(f"Venue Name: {venue.name}\nAddress: {venue.address}\nZip Code: {venue.zip_code}\n"
                     f"Phone Number: {venue.phone}\nWeb Address: {venue.web}\nEmail: {venue.email}\n\n\n")
    response.writelines(lines)
    return response


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    venues = Venue.objects.all()

    # Create a csv writer and Add column headings to the csv writer
    writer = csv.writer(response)
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone Number', 'Web Address', 'Email'])

    for venue in venues:
        writer.writerow([venue.name, venue.address,venue.zip_code, venue.phone, venue.web, venue.email])
    return response


def venue_pdf(request):
    # Create a byte stream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj  = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont('Helvetica', 14)

    # Designate the model and Create blank list
    venues = Venue.objects.all()
    lines = []

    for venue in venues:
        lines.append(f"Venue Name: {venue.name}")
        lines.append(f"Address: {venue.address}")
        lines.append(f"Zip Code: {venue.zip_code}")
        lines.append(f"Phone Number: {venue.phone}")
        lines.append(f"Web Address: {venue.web}")
        lines.append(f"Email: {venue.email}")
        lines.append("")
    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Venues.pdf')


# Generating text file containing all events dynamically
def event_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=events.txt'
    events = Event.objects.all()
    lines = []
    for event in events:
        lines.append(f"Event Name: {event.name}\nAddress: {event.address}\nZip Code: {event.zip_code}\n"
                     f"Phone Number: {event.phone}\nWeb Address: {event.web}\nEmail: {event.email}\n\n\n")
    response.writelines(lines)
    return response


def event_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=events.csv'
    events = Event.objects.all()

    # Create a csv writer and Add column headings to the csv writer
    writer = csv.writer(response)
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone Number', 'Web Address', 'Email'])

    for event in events:
        writer.writerow([event.name, event.address, event.zip_code, event.phone, event.web, event.email])
    return response


def event_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj  = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont('Helvetica', 14)

    # Designate the model and Create blank list
    events = Event.objects.all()
    lines = []
    for event in events:
        lines.append(f"Venue Name: {event.name}")
        lines.append(f"Address: {event.address}")
        lines.append(f"Zip Code: {event.zip_code}")
        lines.append(f"Phone Number: {event.phone}")
        lines.append(f"Web Address: {event.web}")
        lines.append(f"Email: {event.email}")
        lines.append("")

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Venues.pdf')

