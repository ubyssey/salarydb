#!/bin/bash

# Start the server
sudo chown salarydb ${BASH_SOURCE%/*}/gunicorn_start
sudo chmod u+x ${BASH_SOURCE%/*}/gunicorn_start
sudo -u salarydb -H sh -c "${BASH_SOURCE%/*}/gunicorn_start"
