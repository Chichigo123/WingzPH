#!/bin/bash
cd ..

echo "Running db setup!"
echo "Deleting all Rides and Ride_events table data"

# Flush table data
python manage.py clear_ridelist_tables

echo "Creating bulk users"
python manage.py create_bulk_user

echo "Creating bulk rides"
python manage.py create_bulk_rides

echo "Done!"

read -p "Press Enter to exit..."
