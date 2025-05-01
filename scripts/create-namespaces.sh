#!/bin/bash

# Create namespaces for common tools
namespaces=("api" "data" "monitoring" "networking" "security" "storage" )
for ns in "${namespaces[@]}"; do
  echo "Create namespace $ns..."
  nsfile=./$ns/namespace.yaml
  kubectl create -f $nsfile
  kubectl get ns fw-$ns -o yaml
done
