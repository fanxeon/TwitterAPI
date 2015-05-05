#!/bin/bash
# Destroys cluster (idempotent operation).

# Exit on first non-zero command return
set -e

### Initialization stage

# Config
DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
source $DIR/platform-config.sh
BASE_DIR=$DIR/$PLATFORM

### Ansible stage
cd $BASE_DIR/ansible

# Remove template generated files
rm -f hosts

### Terraform stage
cd $BASE_DIR/terraform

# Destroy cluster
terraform destroy

# Remove template generated files
rm -f cloud-config.yaml
rm -f terraform.tfvars

### Finalization stage
cd $BASE_DIR

echo 'Cluster destruction complete'
