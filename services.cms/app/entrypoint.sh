#!/bin/sh

echo "Migrating database..."

# python manage.py flush --no-input
python manage.py migrate
echo "Migration is completed..."
echo "Adding initial data to database..."
python manage.py loaddata initial_data.json
echo "Adding succeeded..."
echo "Creating super user..."
python manage.py createsuperuser --noinput # use DJANGO_SUPERUSER_EMAIL & DJANGO_SUPERUSER_PASSWORD to createsuperuser
echo "Creating super user succeeded..."
# echo "Pushing disease data to server"
# python manage.py loaddata diseases.json
echo "Server is starting..."
python manage.py runserver 0.0.0.0:8000
echo "Starting server succeeded..."
exec "$@"