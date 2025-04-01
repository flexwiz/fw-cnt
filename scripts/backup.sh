#!/bin/bash
# Backup important directories
SOURCE="$1"
DESTINATION="$2"
TIMESTAMP=$(date +"%Y%m%d%H%M")
tar -czf $DESTINATION/backup_$TIMESTAMP.tar.gz $SOURCE
echo "Backup of $SOURCE completed at $DESTINATION/backup_$TIMESTAMP.tar.gz"
