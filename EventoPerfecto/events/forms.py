from django import forms
from django.forms import ModelForm
from .models import Venue


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

        # from_attribute =
