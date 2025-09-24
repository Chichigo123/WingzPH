import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from ridelist.models import Ride, Ride_Event, User  # Example: import your model


class Command(BaseCommand):
    help = "Create test rides."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Creating rides in bulk.!"))

        Ride_Event.objects.all().delete()
        Ride.objects.all().delete()

        riders = User.objects.filter(role="RIDER")
        drivers = User.objects.filter(role="DRIVER")
        ride_objects = []
        ride_events = []
        years = [2023, 2024, 2025]

        for year in years:
            ride_objects += [
                Ride(
                    # Set initial status of all Rides is pickup
                    status="PICKUP",
                    id_rider=riders[random.randint(0, 49)],
                    id_driver=drivers[random.randint(0, 49)],
                    pickup_latitude=random.random() * 1000 + (i / 100),
                    pickup_longitude=random.random() * 1000 + (i / 100),
                    dropoff_latitude=random.random() * 1000 + (i / 100),
                    dropoff_longitude=random.random() * 1000 + (i / 100),
                    pickup_time=datetime(
                        year,
                        random.randint(1, 12),
                        random.randint(1, 28),
                        random.randint(1, 12),
                        0,
                        0,
                    ),
                )
                for i in range(0, 1000)
            ]

        # create 50 rides dated today
        ride_objects += [
            Ride(
                status="PICKUP",
                id_rider=riders[i],
                id_driver=drivers[i],
                pickup_latitude=random.random() * 1000 + (i / 100),
                pickup_longitude=random.random() * 1000 + (i / 100),
                dropoff_latitude=random.random() * 1000 + (i / 100),
                dropoff_longitude=random.random() * 1000 + (i / 100),
                pickup_time=datetime.now(),
            )
            for i in range(0, 50)
        ]

        Ride.objects.bulk_create(ride_objects)

        rides = Ride.objects.all().order_by("id_ride")

        # Create initial ride_events with Pickup status
        for ride in rides:
            ride_events += [
                Ride_Event(
                    id_ride=ride,
                    description=Ride_Event.STATUS_CHANGE_MESSAGE[ride.status],
                )
            ]

        Ride_Event.objects.bulk_create(ride_events)

        # Set created_at to last 48 hours
        time_48_hours = datetime.now() - timedelta(hours=48)
        Ride_Event.objects.update(created_at=time_48_hours)

        # Now let us get half of the Rides and change status DROPOFF
        # created_at is set to auto_now_add, so we now have half of the Rides with more than an hour trip
        ride_events = []
        count_half_rides = int(Ride.objects.count() / 2)
        half_rides = Ride.objects.all().order_by("id_ride")[:count_half_rides]
        Ride.objects.filter(id_ride__in=half_rides.values("id_ride")).update(
            status="DROPOFF"
        )

        for ride in half_rides:
            ride_events += [
                Ride_Event(
                    id_ride=ride,
                    description=Ride_Event.STATUS_CHANGE_MESSAGE["DROPOFF"],
                )
            ]
        Ride_Event.objects.bulk_create(ride_events)
        self.stdout.write(self.style.SUCCESS("Script finished successfully!"))
