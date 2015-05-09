variable "peer_node_count" {
  description = "Number of nodes"
}
variable "peer_name_prefix" {
  description = "Node name's prefix"
}
variable "availability_zone" {
  description = "OpenStack availability zone"
}
variable "keypair" {
  description = "OpenStack keypair"
}
variable "flavor_id" {
  description = "OpenStack instance flavor id"
}
variable "domain" {
  description = "Domain for nodes"
}
variable "subdomain" {
  description = "Sub-domain for nodes"
}
variable "dns_ttl" {
  description = "Domain record's ttl"
}
variable "image_id" {
  description = "OpenStack image id"
}
variable "volume_size" {
  description = "Volume size"
}
