#!/bin/bash
# Ensure critical services are always running by automating health checks and restarts.
SERVICE=$1
if pgrep $SERVICE >/dev/null 2>&1
then
  echo "$SERVICE is running."
else
  echo "$SERVICE is not running. Attempting to start..."
  sudo systemctl start $SERVICE
  if pgrep $SERVICE >/dev/null 2>&1
  then
    echo "$SERVICE started successfully."
  else
    echo "Failed to start $SERVICE."
  fi
fi
