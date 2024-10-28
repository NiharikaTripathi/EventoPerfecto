from django.db import models
from django.contrib.auth.models import User

# Venue models
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Phone Number', max_length=25)
    web = models.URLField('Website Address')
    email = models.EmailField('Email')
    owner = models.IntegerField('Venue Owner', blank=False, default=1)

    def __str__(self):
        return self.name


# Event models
class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField('Venue', max_length=120)
    manager = models.ForeignKey( User, blank=True, null=True, on_delete=models.SET_NULL, related_name='event_manager')
    description = models.TextField('Event Description', max_length=120)
    attendees = models.ManyToManyField(User, blank=True, related_name='event_attendees')

    def __str__(self):
        return self.name