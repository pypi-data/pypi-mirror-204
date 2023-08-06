data "scaleway_instance_server" "main" {
  name = var.instance_name
}

data "scaleway_vpc_public_gateway" "main" {
  name = var.vpc_name
}

data scaleway_vpc_private_network "service" {
  name = var.lan_name
}

data scaleway_vpc_gateway_network "service_net" {
    gateway_id = data.scaleway_vpc_public_gateway.main.id
    private_network_id = data.scaleway_vpc_private_network.service.id
}

resource "scaleway_instance_private_nic" "service_nic" {
  server_id = data.scaleway_instance_server.main.id
  private_network_id = data.scaleway_vpc_private_network.service.id
}

resource "time_sleep" "wait_5_seconds_after_service_nic" {
  depends_on = [scaleway_instance_private_nic.service_nic]
  create_duration = "5s"
}

resource scaleway_vpc_public_gateway_dhcp_reservation main {
    gateway_network_id = data.scaleway_vpc_gateway_network.service_net.id
    mac_address = scaleway_instance_private_nic.service_nic.mac_address
    ip_address = var.lan_ip
    depends_on = [time_sleep.wait_5_seconds_after_service_nic]
}

resource scaleway_vpc_public_gateway_pat_rule service_pat {
    gateway_id = data.scaleway_vpc_public_gateway.main.id
    private_ip = var.lan_ip
    private_port = var.lan_port
    public_port = var.wan_port
    protocol = var.protocol
    depends_on = [scaleway_vpc_public_gateway_dhcp_reservation.main]
}

locals {
  default_ssh = [
    "ufw allow ssh",
    "ufw --force enable"
  ]
  add_new_rules = [
    for ip in var.allowed_ips : "ufw allow from ${ip} to any port ${var.lan_port}"
  ]
  network_ips = [
    for ip in var.allowed_ips : (
      can(cidrnetmask(ip)) ? cidrsubnet(ip, 0, 0) : ip
    )
  ]
}

data "scaleway_instance_server" "instance" {
  name = var.instance_name
}

data scaleway_vpc_private_network "mongo_net" {
  name = var.vpc_name
}

resource "null_resource" "ufw_status" {
  triggers = {
    # new_ips = jsonencode(var.allowed_ips)
    always_run = timestamp()
  }

  provisioner "remote-exec" {
    inline = concat(
      local.add_new_rules,
      ["for ip in $(ufw status | grep '${var.lan_port}' | awk '{print $3}'); do if ! echo \"${join(" ", local.network_ips)}\" | grep -q -w \"$ip\"; then ufw delete allow from $ip to any port 27017; fi; done"]
    )

    connection {
      type        = "ssh"
      user        = "root"
      private_key = file(var.ssh_private_key)
      host        = var.lan_ip

      bastion_host        = var.wan_ip
      bastion_port        = 59999
      bastion_user        = "bastion"
      bastion_private_key = file(var.ssh_private_key)

      timeout              = "5m"   # Maximum time to wait for the connection to become available
    }
  }
}

