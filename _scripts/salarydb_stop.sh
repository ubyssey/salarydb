#!/bin/bash

# Stop the server
if [ -f run/salarydb.pid ]; then
  sudo kill `cat run/salarydb.pid`
fi
