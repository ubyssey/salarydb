#!/bin/bash

NAME="salarydb"
SOCKFILE=/var/webapps/salarydb/run/gunicorn.sock
PIDFILE=/var/webapps/salarydb/run/salarydb.pid
LOGFILE=/var/webapps/salarydb/logs/gunicorn-error.log
USER=salarydb
GROUP=webapps
NUM_WORKERS=3
DJANGO_PROJECT_DIR=/var/webapps/salarydb/salarydb
DJANGO_WSGI_MODULE=salarydb.wsgi

# Activate the virtual environment
cd $DJANGO_PROJECT_DIR
cd ../
source bin/activate
export PYTHONPATH=$DJANGO_PROJECT_DIR:$PYTHONPATH

# Install dependencies

pip install -r /var/webapps/salarydb/requirements.txt

# Start gunicorn daemon

echo "Starting $NAME as `whoami`"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file $LOGFILE \
  --daemon \
  --pid $PIDFILE
