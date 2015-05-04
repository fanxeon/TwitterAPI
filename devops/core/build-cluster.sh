#!/bin/bash
# Builds cluster (idempotent operation).

### Initialization stage

# Config
BASE_DIR=$(pwd)
TEMPLATE_DIR=$BASE_DIR/templates

# Source env
source $BASE_DIR/cluster-config.sh

# Applies jinja2 template with environment variables.
# 
# Arguments:
#   Jinja2 template
# Returns:
#   Applied template
apply_template() {
  env | j2 -f env $1
}

### Terraform stage
cd $BASE_DIR/terraform

# Define cloud config
if [ ! -f ./cloud-config.yaml ]; then
  export CLUSTER_DISCOVERY_URL=$(curl -s \
    "https://discovery.etcd.io/new?size=$ETCD_MASTER_COUNT")

  apply_template $TEMPLATE_DIR/cloud-config.yaml.j2 > cloud-config.yaml
fi

# Define terraform config
apply_template $TEMPLATE_DIR/terraform.tfvars.j2 > terraform.tfvars

# Provision/update cluster
terraform apply

# Retrieve outputs
export PEER_COUNT=$(terraform output peer_count)

### Ansible stage
cd $BASE_DIR/ansible

# Generate hosts
apply_template $TEMPLATE_DIR/hosts.j2 > hosts

# Configure cluster
ansible-playbook -i hosts site.yml

### Finalization stage
cd $BASE_DIR

echo 'Cluster build complete'