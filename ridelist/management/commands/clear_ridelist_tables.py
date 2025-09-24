from django.core.management.base import BaseCommand

from ridelist.models import Ride, Ride_Event  # Example: import your model


class Command(BaseCommand):
    help = "Delete all entries from Ride, Ride_Events."

    def handle(self, *args, **options):
        # Your script logic here
        self.stdout.write(self.style.SUCCESS("Deleting all ride entries!"))
        Ride_Event.objects.all().delete()
        Ride.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Script finished successfully!"))
