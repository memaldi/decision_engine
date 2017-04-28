#!/bin/sh
export DJANGO_SETTINGS_MODULE=decision_engine.settings

./manage.py makemigrations ;
./manage.py migrate ;
./manage.py runserver 0.0.0.0:8000 ;
