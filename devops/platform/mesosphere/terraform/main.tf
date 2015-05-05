# Configure openstack
provider "openstack" {
  # Obtain all configuration from environment variables
  # NOTE: Intentionally left blank.
}

# Configure wildcard DNS
resource "dnsimple_record" "dom" {
  domain = "${var.domain}"
  name = "*.${var.subdomain}"
  value = "${element(openstack_compute_instance_v2.master.*.access_ip_v4, count.index)}"
  type = "A"
  ttl = "${var.dns_ttl}"
  count = "${var.master_node_count}"
}

# Configure master DNS records                                                   
resource "dnsimple_record" "master" {                                            
  domain = "${var.domain}"                                                       
  name = "${element(openstack_compute_instance_v2.master.*.name, count.index)}.${var.subdomain}"
  value = "${element(openstack_compute_instance_v2.master.*.access_ip_v4, count.index)}"
  type = "A"                                                                     
  ttl = "${var.dns_ttl}"
  count = "${var.master_node_count}"                                             
} 

# Configure slave DNS records                                                   
resource "dnsimple_record" "slave" {                                            
  domain = "${var.domain}"                                                       
  name = "${element(openstack_compute_instance_v2.slave.*.name, count.index)}.${var.subdomain}"
  value = "${element(openstack_compute_instance_v2.slave.*.access_ip_v4, count.index)}"
  type = "A"                                                                     
  ttl = "${var.dns_ttl}"
  count = "${var.slave_node_count}"                                             
} 

# Configure master instances
resource "openstack_compute_instance_v2" "master" {
  name = "${var.master_name_prefix}${count.index}"
  availability_zone = "${var.availability_zone}"
  image_id = "${var.image_id}"
  flavor_id = "${var.flavor_id}"
  key_pair = "${var.keypair}"
  security_groups = ["${openstack_compute_secgroup_v2.sec.name}"]
  count = "${var.master_node_count}"
}
# Configure slave instances
resource "openstack_compute_instance_v2" "slave" {
  name = "${var.slave_name_prefix}${count.index}"
  availability_zone = "${var.availability_zone}"
  image_id = "${var.image_id}"
  flavor_id = "${var.flavor_id}"
  key_pair = "${var.keypair}"
  security_groups = ["${openstack_compute_secgroup_v2.sec.name}"]
  count = "${var.slave_node_count}"
}

# Configure security groups
resource "openstack_compute_secgroup_v2" "sec" {
  name = "sec"
  description = "Security group"

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
