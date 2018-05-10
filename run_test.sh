#!/usr/bin/env bash

# make sure there is not table before creating
python manage.py delete_session_table
# create dynamo session stable
python manage.py create_session_table

python manage.py test