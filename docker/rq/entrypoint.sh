#!/bin/sh
export DJANGO_SETTINGS_MODULE=decision_engine.settings

./manage.py rqworker default ;
