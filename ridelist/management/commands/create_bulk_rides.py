from datetime import datetime

from django.core.management.base import BaseCommand

from ridelist.models import (Ride, Ride_Event,  # Example: import your model
                             User)


class Command(BaseCommand):
    help = "Create test rides."

    def handle(self, *args, **options):
        # Your script logic here
        self.stdout.write(self.style.SUCCESS("Creating rides in bulk.!"))

        riders = User.objects.filter(role="RIDER")
        drivers = User.objects.filter(role="DRIVER")

        objects = [
            Ride(
                status="PICKUP",
                id_rider=riders[i],
                id_driver=drivers[i],
                pickup_latitude=123 + (i / 100),
                pickup_longitude=456 + (i / 100),
                dropoff_latitude=789 + (i / 100),
                dropoff_longitude=901 + (i / 100),
                pickup_time=datetime(2025, 1, i, 9, 0, 0),
            )
            for i in range(1, 10)
        ]

        objects += [
            Ride(
                status="EN_ROUTE",
                id_rider=riders[i],
                id_driver=drivers[i],
                pickup_latitude=123 + (i / 100),
                pickup_longitude=456 + (i / 100),
                dropoff_latitude=789 + (i / 100),
                dropoff_longitude=901 + (i / 100),
                pickup_time=datetime(2025, 1, i, 9, 0, 0),
            )
            for i in range(11, 21)
        ]

        objects += [
            Ride(
                status="DROPOFF",
                id_rider=riders[i],
                id_driver=drivers[i],
                pickup_latitude=123 + (i / 100),
                pickup_longitude=456 + (i / 100),
                dropoff_latitude=789 + (i / 100),
                dropoff_longitude=901 + (i / 100),
                pickup_time=datetime(2025, 1, i, 9, 0, 0),
            )
            for i in range(21, 31)
        ]

        # create 10 rides dated today
        objects += [
            Ride(
                status="PICKUP",
                id_rider=riders[i],
                id_driver=drivers[i],
                pickup_latitude=123 + (i / 100),
                pickup_longitude=456 + (i / 100),
                dropoff_latitude=789 + (i / 100),
                dropoff_longitude=901 + (i / 100),
                pickup_time=datetime.now(),
            )
            for i in range(31, 41)
        ]

        Ride.objects.bulk_create(objects)
        self.stdout.write(self.style.SUCCESS("Script finished successfully!"))
