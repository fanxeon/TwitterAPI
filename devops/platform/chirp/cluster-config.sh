### Cluster configuration

# Openstack instance availablity zone
export INS_AVAILABILITY_ZONE="melbourne-qh2-uom"
# Openstack volume availablity zone
export VOL_AVAILABILITY_ZONE="melbourne-qh2"
# Openstack instance flavor id
export FLAVOR_ID="1"
# Openstack keypair
export KEYPAIR="team19"
# Number of nodes
export PEER_NODE_COUNT=3
# Node name's prefix
export PEER_NAME_PREFIX="b-"
# Domain for nodes
export DOMAIN="t19.ninja"
# Sub-domain for nodes
export SUBDOMAIN="chi"
# Domain record's TTL
export DNS_TTL=5
# Image ID (Ubuntu 14.04 LTS)
export IMAGE_ID="eeedf697-5a41-4d91-a478-01bb21e32cbe"
# Etcd master count
export ETCD_MASTER_COUNT=3
# Volume size for nodes
export VOLUME_SIZE=50
# Ansible ssh host checking
export ANSIBLE_HOST_KEY_CHECKING=False
