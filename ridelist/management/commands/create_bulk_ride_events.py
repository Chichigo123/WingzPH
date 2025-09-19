from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ridelist.models import (Ride, Ride_Event,  # Example: import your model
                             User)


class Command(BaseCommand):
    help = "Create test ride events."

    def handle(self, *args, **options):
        # Your script logic here
        self.stdout.write(self.style.SUCCESS("Creating ride events in bulk.!"))

        latest_rides = Ride.objects.filter(pickup_time__date=datetime.now())[:10]
        objects = []
        for ride in latest_rides:
            objects += [
                Ride_Event(
                    id_ride=ride,
                    description="Changed status to PICKUP",
                    created_at=datetime.now(),
                )
            ]
            objects += [
                Ride_Event(
                    id_ride=ride,
                    description="Changed status to EN_ROUTE",
                    created_at=datetime.now(),
                )
            ]
            objects += [
                Ride_Event(
                    id_ride=ride,
                    description="Changed status to DROPOFF",
                    created_at=datetime.now(),
                )
            ]

        Ride_Event.objects.bulk_create(objects)

        # create ride events for the rest of the old rides
        old_rides = Ride.objects.exclude(id_ride__in=(latest_rides.values("id_ride")))

        objects = []
        for ride in old_rides:
            objects += [
                Ride_Event(id_ride=ride, description="Changed status to PICKUP")
            ]
            objects += [
                Ride_Event(id_ride=ride, description="Changed status to EN_ROUTE")
            ]
            objects += [
                Ride_Event(id_ride=ride, description="Changed status to DROPOFF")
            ]

        Ride_Event.objects.bulk_create(objects)

        old_ride_events = Ride_Event.objects.order_by("id_ride")[30:]
        time_48_hours = datetime.now() - timedelta(hours=48)
        Ride_Event.objects.filter(id_ride__in=old_ride_events.values("id_ride")).update(
            created_at=time_48_hours
        )

        self.stdout.write(self.style.SUCCESS("Script finished successfully!"))
