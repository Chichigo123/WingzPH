#!/bin/bash
cd ..
echo "Running reset db!"
echo "Dropping all tables"

# Flush table data
python manage.py migrate ridelist zero

echo "Creating migrations"
python manage.py makemigrations

echo "Unapply and Applying migrations"
python manage.py migrate ridelist zero
python manage.py migrate

echo "Creating bulk users"
python manage.py create_bulk_user

echo "Creating bulk rides"
python manage.py create_bulk_rides

echo "Done!"

read -p "Press Enter to exit..."
