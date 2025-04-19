#!/bin/bash
# Generate SSH key and copy to remote servers
REMOTE_USER=$1
REMOTE_HOSTS=($2) # List of remote hosts: "server1.flexwiz.io" "server2.flexwiz.io"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
for HOST in "${REMOTE_HOSTS[@]}"; do
  ssh-copy-id $REMOTE_USER@$HOST
  echo "SSH key copied to $REMOTE_USER@$HOST"
done
