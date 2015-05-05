### Cluster configuration

# Openstack availablity zone
export AVAILABILITY_ZONE="sa"
# Openstack instance flavor id
export FLAVOR_ID="1"
# Openstack keypair
export KEYPAIR="team19"
# Number of master nodes
export MASTER_NODE_COUNT=3
# Node master name's prefix
export MASTER_NAME_PREFIX="m-"
# Number of slave nodes
export SLAVE_NODE_COUNT=3
# Node slave name's prefix
export SLAVE_NAME_PREFIX="s-"
# Domain for nodes
export DOMAIN="t19.ninja"
# Sub-domain for nodes
export SUBDOMAIN="mes"
# Domain record's TTL
export DNS_TTL=5
# Image ID (Ubuntu 14.04 LTS)
export IMAGE_ID="eeedf697-5a41-4d91-a478-01bb21e32cbe"
# Ansible ssh host checking
export ANSIBLE_HOST_KEY_CHECKING=False
