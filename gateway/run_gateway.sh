#!/bin/bash
#
# Launch the router. Put this file in /srv/smsBEST/bin.
#
cd /srv/smsBEST
source bin/activate
cd gateway
python manage.py runrouter

