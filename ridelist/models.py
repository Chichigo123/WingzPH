from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(models.Model):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        DRIVER = "DRIVER", "driver"
        RIDER = "RIDER", "rider"

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=Roles.choices)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Ride(models.Model):
    class RideStatus(models.TextChoices):
        EN_ROUTE = "EN_ROUTE", "en-route"
        PICKUP = "PICKUP", "pickup"
        DROPOFF = "DROPOFF", "dropoff"

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=20, choices=RideStatus.choices, default=RideStatus.PICKUP
    )
    id_rider = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="rides_as_rider"
    )
    id_driver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="rides_as_driver"
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"{self.id_rider} - {self.status}"


class Ride_Event(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride, on_delete=models.PROTECT, related_name="ride_events"
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_ride_event} - {self.description}@{self.created_at}"
