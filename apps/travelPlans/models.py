from django.db import models
from ..loginAndRegistration.models import *
import datetime

# Create your models here.
class travelsManager(models.Manager):
    def travelsValidator(self,data, user_id):
        errors={}
        if len(data['destination']) < 1:
            errors['destination'] = "Please enter a destination."
        elif len(data['destination']) > 254:
            errors['destination'] = "Destination cannot be over 255 characters long."
        if len(data['desc']) < 1:
            errors['desc'] = "Please enter a description."
        elif len(data['desc']) > 254:
            errors['desc'] = "Description cannot be over 255 characters long."
        if len(data['startdate']) < 1:
            errors['startdate'] = "When does the trip begin?"
        else:
            startdate = datetime.datetime.strptime(data['startdate'], '%Y-%m-%d')
            if datetime.datetime.now()>startdate:
                errors['startdate'] = "The trip must start in a future date."
        if len(data['enddate']) < 1:
            errors['enddate'] = "When does the trip end?"
        else:
            enddate = datetime.datetime.strptime(data['enddate'], '%Y-%m-%d')
            if startdate>enddate:
                errors['enddate'] = "The trip must end after the start date."

        if not errors:
            travels.objects.create(destination=data['destination'], desc=data['desc'], startdate=startdate, enddate=enddate, traveler=User.objects.get(id=user_id))

        return errors

class travels(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    traveler = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    joiners = models.ManyToManyField(User, related_name="joined_trips")

    objects = travelsManager()

    def __repr__(self):
        return "<User: {}|{}>".format(self.id, self.destination)
