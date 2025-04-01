#!/bin/bash
# Update and upgrade system packages
echo "Starting system update..."
sudo apt-get update -y && sudo apt-get upgrade -y
echo "System update completed."
