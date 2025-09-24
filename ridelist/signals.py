from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ride, Ride_Event


@receiver(post_save, sender=Ride)
def ride_updated_handler(sender, instance, created, **kwargs):
    """
    Creates a ride_event on status update or create.
    """

    Ride_Event.objects.create(
        id_ride=instance, description=Ride_Event.STATUS_CHANGE_MESSAGE[instance.status]
    )
