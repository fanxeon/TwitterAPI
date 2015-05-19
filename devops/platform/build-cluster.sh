#!/bin/bash
# Builds cluster (idempotent operation).

# Exit on first non-zero command return
set -e

### Initialization stage

# Config
DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
source $DIR/platform-config.sh
BASE_DIR=$DIR/$PLATFORM
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

# Wait until all nodes have SSH ready
terraform output ips | while read -r line ; do
  echo "Checking for OpenSSH start on: $line"
  while ! ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ConnectTimeout=10 -q ubuntu@$line exit < /dev/null ; do
    echo "Timeout, waiting 10 seconds before next attempt"
    sleep 10
    echo "Checking for OpenSSH start on: $line"
  done
  echo "OpenSSH running on: $line"
done

### Ansible stage
cd $BASE_DIR/ansible

# Generate hosts
$BASE_DIR/gen-hostfile.py \
  $BASE_DIR/terraform/terraform.tfstate \
  > hosts

# Configure cluster
ansible-playbook -i hosts site.yml

### Finalization stage
cd $BASE_DIR

echo 'Cluster build complete'
