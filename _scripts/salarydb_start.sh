#!/bin/bash

GUNICORN_SCRIPT=/var/webapps/salarydb/_scripts/gunicorn_start.sh

# Start the server
sudo chown salarydb $GUNICORN_SCRIPT
sudo chmod u+x $GUNICORN_SCRIPT

sudo supervisorctl start salarydb
