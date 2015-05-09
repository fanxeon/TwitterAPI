# Configure openstack
provider "openstack" {
  # Obtain all configuration from environment variables
  # NOTE: Intentionally left blank.
}

# Configure wildcard DNS
resource "dnsimple_record" "dom" {
  domain = "${var.domain}"
  name = "*.${var.subdomain}"
  value = "${element(openstack_compute_instance_v2.peer.*.access_ip_v4, count.index)}"
  type = "A"
  ttl = "${var.dns_ttl}"
  count = "${var.peer_node_count}"
}

# Configure peer DNS records                                                   
resource "dnsimple_record" "peer" {                                            
  domain = "${var.domain}"                                                       
  name = "${element(openstack_compute_instance_v2.peer.*.name, count.index)}.${var.subdomain}"
  value = "${element(openstack_compute_instance_v2.peer.*.access_ip_v4, count.index)}"
  type = "A"                                                                     
  ttl = "${var.dns_ttl}"
  count = "${var.peer_node_count}"                                             
} 

# Configure peer instances
resource "openstack_compute_instance_v2" "peer" {
  name = "${var.peer_name_prefix}${count.index+1}"
  availability_zone = "${var.availability_zone}"
  image_id = "${var.image_id}"
  flavor_id = "${var.flavor_id}"
  key_pair = "${var.keypair}"
  security_groups = ["${openstack_compute_secgroup_v2.peer.name}"]
  count = "${var.peer_node_count}"

  # Cloud init
  user_data = "${file(\"cloud-config.yaml\")}"
}

# Configure peer security groups
resource "openstack_compute_secgroup_v2" "peer" {
  name = "peer"
  description = "Peer security group"

  # Enable SSH to all
  rule {
    from_port = 22
    to_port = 22
    ip_protocol = "tcp"
    cidr = "0.0.0.0/0"
  }
  # Enable all ports to own group
  rule {
    from_port = 1
    to_port = 65535
    ip_protocol = "tcp"
    self = "true"
  }
  rule {
    from_port = 1
    to_port = 65535
    ip_protocol = "udp"
    self = "true"
  }
}
