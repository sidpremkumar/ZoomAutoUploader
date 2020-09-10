#!/bin/bash

while :
do
    echo "Starting check for new recordings..."
    python3.6 ./zoomautouploader/main.py
    echo "Finished check...sleeping for 15 minutes"
    sleep 15m
done