#!/bin/bash

# Start the server
sudo chown salarydb ${BASH_SOURCE%/*}/gunicorn_start.sh
sudo chmod u+x ${BASH_SOURCE%/*}/gunicorn_start.sh
sudo -u salarydb -H sh -c "${BASH_SOURCE%/*}/gunicorn_start.sh"
