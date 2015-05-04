#!/bin/bash
# Destroys cluster (idempotent operation).

### Initialization stage

# Config
BASE_DIR=$(pwd)

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
