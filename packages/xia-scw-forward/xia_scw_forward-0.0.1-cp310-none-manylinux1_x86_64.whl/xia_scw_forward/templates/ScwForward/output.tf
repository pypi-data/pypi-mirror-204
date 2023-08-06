output "project_id" {
  value = var.project_id
}

output "vpc_name" {
  value = var.vpc_name
}

output "instance_name" {
  value = var.instance_name
}

output "service_name" {
  value = var.service_name
}

output "lan_name" {
  value = data.scaleway_vpc_private_network.service.name
}

output "lan_ip" {
  value = scaleway_vpc_public_gateway_pat_rule.service_pat.private_ip
}

output "wan_port" {
  value = scaleway_vpc_public_gateway_pat_rule.service_pat.public_port
}

output "protocol" {
  value = scaleway_vpc_public_gateway_pat_rule.service_pat.protocol
}

output "lan_port" {
  value = scaleway_vpc_public_gateway_pat_rule.service_pat.private_port
}

output "allowed_ips" {
  value = var.allowed_ips
}
