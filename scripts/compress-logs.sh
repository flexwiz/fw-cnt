#!/bin/bash
# Rotate and compress logs
LOG_DIR="/var/log/myapp/"
BACKUP_DIR="/var/log/myapp/backup/"
TIMESTAMP=$(date +"%Y%m%d")
mkdir -p $BACKUP_DIR
find $LOG_DIR -name "*.log" -type f -exec mv {} $BACKUP_DIR \;
find $BACKUP_DIR -name "*.log" -type f -exec gzip {} \;
echo "Log rotation and compression completed."
