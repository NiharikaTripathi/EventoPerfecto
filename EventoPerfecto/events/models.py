from django.db import models

# Event models
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Phone Number', max_length=25)
    web = models.URLField('Website Address')
    email = models.EmailField('Email')

    def __str__(self):
        return self.name

# Event models
class MyClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=120)
    last_name = models.CharField('Last Name', max_length=120)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + " " + self.last_name

# Event models
class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField('Venue', max_length=120)
    manager = models.CharField('Manager Name', max_length=120)
    description = models.TextField('Event Description', max_length=120)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name