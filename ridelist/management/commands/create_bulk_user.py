from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from ridelist.models import (Ride, Ride_Event,  # Example: import your model
                             User)


class Command(BaseCommand):
    help = "Create test users."

    def handle(self, *args, **options):
        # Your script logic here
        self.stdout.write(self.style.SUCCESS("Creating test data in bulk.!"))

        objects = [
            User(
                role="ADMIN",
                first_name=f"John_{i}",
                last_name=f"Doe_{i}",
                email=f"john_doe_{i}@email.com",
                phone_number="123456789",
                # username=f'John_{i}_doe', password=make_password(f'test{i}')
            )
            for i in range(50)
        ]

        objects += [
            User(
                role="DRIVER",
                first_name=f"Mark_{i}",
                last_name=f"Lasso_{i}",
                email=f"mark_lasso_{i}@email.com",
                phone_number="123456789",
                #   username=f'Mark_{i}_lasso', password=make_password(f'test{i}')
            )
            for i in range(50)
        ]

        objects += [
            User(
                role="RIDER",
                first_name=f"Tanya_{i}",
                last_name=f"Smith_{i}",
                email=f"tanya_smith_{i}@email.com",
                phone_number="123456789",
                #    username=f'Tanya_{i}_smith', password=make_password(f'test{i}')
            )
            for i in range(50)
        ]

        User.objects.bulk_create(objects)
        self.stdout.write(self.style.SUCCESS("Script finished successfully!"))
