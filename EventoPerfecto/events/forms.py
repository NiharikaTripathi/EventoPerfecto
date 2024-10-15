from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Create forms for models
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email' )  # "__all__"
        labels  = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Venue Name Here'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address of the venue'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone Number'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Web address'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'})
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees','description' )  # "__all__"
        labels  = {
            'name': 'Event Name :',
            'event_date': 'Event Date (YYYY-MM-DD HH:MM:SS) :',
            'venue': 'Venue Name :',
            'manager': 'Manager :',
            'description': 'Description of the Event :',
            'attendees' : 'Attendees of the Event :'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Event Name Here'}),
            'event_date': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'Date of the event'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue Name'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees of the Event'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description of the Event'}),

        }
