output "ips" {
  value = "${join("\n", openstack_compute_instance_v2.peer.*.access_ip_v4)}"
}
