#!/bin/bash
# Delete files older than 7 days in /tmp
find /tmp -type f -mtime +7 -exec rm -f {} \;
echo "Old temporary files deleted."
