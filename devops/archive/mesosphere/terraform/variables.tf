variable "master_node_count" {
  description = "Number of master nodes"
}
variable "master_name_prefix" {
  description = "Node master name's prefix"
}
variable "slave_node_count" {
  description = "Number of slave nodes"
}
variable "slave_name_prefix" {
  description = "Node slave name's prefix"
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
