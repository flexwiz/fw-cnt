#!/bin/bash
# Monitor disk usage and send an alert if usage exceeds 80%
THRESHOLD=80
ADMIN_EMAIL="admin@sample.fr"
df -H | awk '{ print $5 " " $1 }' | while read output; do
  usage=$(echo $output | awk '{ print $1}' | sed 's/%//')
  partition=$(echo $output | awk '{ print $2 }')
  if [ $usage -ge $THRESHOLD ]; then
    echo "Running out of space \"$partition ($usage%)\" on $(hostname) as on $(date)" | \
    mail -s "Disk Space Alert: $usage%" $EMAIL
  fi
done
