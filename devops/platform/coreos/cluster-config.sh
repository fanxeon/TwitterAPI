### Cluster configuration

# Openstack availablity zone
export AVAILABILITY_ZONE="sa"
# Openstack instance flavor id
export FLAVOR_ID="1"
# Openstack keypair
export KEYPAIR="team19"
# Number of nodes
export PEER_NODE_COUNT=3
# Node name's prefix
export PEER_NAME_PREFIX="p-"
# Domain for nodes
export DOMAIN="t19.ninja"
# Sub-domain for nodes
export SUBDOMAIN="cor"
# Domain record's TTL
export DNS_TTL=5
# Image ID
export IMAGE_ID="6dbf5466-1e9e-4c52-a295-5f7cb9e3fdb5"
# Etcd master count
export ETCD_MASTER_COUNT=3
# Ansible ssh host checking
export ANSIBLE_HOST_KEY_CHECKING=False
