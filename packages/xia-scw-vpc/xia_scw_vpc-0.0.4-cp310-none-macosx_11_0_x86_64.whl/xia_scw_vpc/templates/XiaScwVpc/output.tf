output "project_id" {
  value = var.project_id
}

output "name" {
  value = scaleway_vpc_private_network.main.name
}

output "type" {
  value = scaleway_vpc_public_gateway.main.type
}

output "ip_id" {
  value = var.ip_id
}

output "lan_name" {
  value = var.lan_name
}

output "lan_ip" {
  value = var.lan_ip
}

output "lan_netmask" {
  value = var.lan_netmask
}

output "bastion_port" {
  value = scaleway_vpc_public_gateway.main.bastion_port
}
