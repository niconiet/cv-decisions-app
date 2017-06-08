#!/bin/sh

cron start

python3 /src/architectureDecisions/manage.py runmodwsgi --port=8080 --user=www-data --group=www-data

