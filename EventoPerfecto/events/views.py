from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from datetime import datetime
from calendar import HTMLCalendar
import csv
import calendar
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.paginator import Paginator

from .forms import VenueForm, EventForm
from .models import Event, Venue, MyClubUser



# Create your views here.
## Calendar Views
def event_calendar(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    # Convert month name to number
    now = datetime.now()
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


#Event Views
# Display all Events
def all_events(request):
    events_list = Event.objects.all().order_by('event_date')
    return render(request, "event_list.html", {'event_list': events_list})

# Add an Event
def add_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_event.html',{'form' :form, 'submitted': submitted})

# Update an Event
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, "update_event.html", {'event': event, 'form': form})

# Delete an Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event:
        event.delete()
        return redirect('list-events')
    else:
        return redirect('list-events')


# Venue Views
# Add a Venue
def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_venue.html',{'form' :form, 'submitted': submitted})

# Display all Venues list
def all_venues(request):
    # venue_list = Venue.objects.all().order_by("?")
    venue_list = Venue.objects.all()
    return render(request, "venues.html", {'venue_list': venue_list})

# Display details of a Venue
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, "show_venue.html", {'venue': venue})

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
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, "update_venue.html", {'venue' : venue, 'form':form})

# Delete a Venue
def delete_venue(request, venue_id):
        venue = Venue.objects.get(pk=venue_id)
        if venue:
            venue.delete()
            return redirect('list-venues')
        else:
            return redirect('list-venues')

# Generating text file containing all venues dynamically
def venue_text(request):
    response = HttpResponse(content_type='textpeError/plain')
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
    # Create a csv writer
    writer = csv.writer(response)
    # Designate the model
    venues = Venue.objects.all()
    # Add column headings to the csv writer
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

    # Designate the model
    venues = Venue.objects.all()

    # Create blank list
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

    # Finish Up
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Venues.pdf')