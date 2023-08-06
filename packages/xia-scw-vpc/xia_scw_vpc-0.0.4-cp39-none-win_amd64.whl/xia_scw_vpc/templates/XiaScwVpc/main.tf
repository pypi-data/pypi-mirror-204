resource "scaleway_vpc_public_gateway_dhcp" "dhcp01" {
  subnet = "${var.lan_ip}/${var.lan_netmask}"
  push_default_route = true
}

resource scaleway_vpc_private_network main {
    name = var.lan_name
}

resource scaleway_vpc_public_gateway main {
    name = var.name
    type = var.type
    ip_id = var.ip_id
    bastion_enabled = true
    bastion_port = var.bastion_port
}

resource scaleway_vpc_gateway_network main {
    gateway_id = scaleway_vpc_public_gateway.main.id
    private_network_id = scaleway_vpc_private_network.main.id
    dhcp_id = scaleway_vpc_public_gateway_dhcp.dhcp01.id
    cleanup_dhcp = true
    enable_masquerade = true
    depends_on = [scaleway_vpc_private_network.main]
}
