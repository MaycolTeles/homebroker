#!/bin/sh

# Script to wait for the PostgreSQL database to be ready before starting the Django application
# And aplly the migrations and collect the static files.

if [ "$DB" = "postgresql" ]
then
    echo "Waiting for postgresql..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python app/manage.py migrate --noinput
python app/manage.py collectstatic --no-input

exec "$@"
