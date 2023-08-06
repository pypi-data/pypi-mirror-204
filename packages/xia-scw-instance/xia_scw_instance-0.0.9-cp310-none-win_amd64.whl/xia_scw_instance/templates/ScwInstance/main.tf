data "scaleway_instance_image" "my_image" {
  name  = var.image
}

resource "scaleway_instance_server" "instance" {
  name = var.name
  type = var.type
  image = data.scaleway_instance_image.my_image.id
  tags = var.tags
  state = var.state
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
  count = (var.state != "stopped" && length(var.lan_ip) > 0) ? 1 : 0
  server_id = scaleway_instance_server.instance.id
  private_network_id = data.scaleway_vpc_private_network.service.id
}

resource "time_sleep" "wait_5_seconds_after_service_nic" {
  count = (var.state != "stopped" && length(var.lan_ip) > 0) ? 1 : 0
  depends_on = [scaleway_instance_private_nic.service_nic]
  create_duration = "5s"
}

resource scaleway_vpc_public_gateway_dhcp_reservation main {
    count = (var.state != "stopped" && length(var.lan_ip) > 0) ? 1 : 0

    gateway_network_id = data.scaleway_vpc_gateway_network.service_net.id
    mac_address = scaleway_instance_private_nic.service_nic[0].mac_address
    ip_address = var.lan_ip
    depends_on = [time_sleep.wait_5_seconds_after_service_nic]
}

locals {
  ufw_ssh = length(var.ssh_hosts) > 0 ? [
    for ip in var.ssh_hosts : "ufw allow from ${ip} to any port 22 proto tcp"
  ] : [
    "ufw allow ssh"
  ]
  ufw_commands = flatten([
    for rule in var.forwards : [
      for ip in rule.allowed_ips : "ufw allow from ${ip} to any port ${rule.lan_port} proto ${rule.protocol}"
    ]
  ])
}

resource scaleway_vpc_public_gateway_pat_rule service_pat {
    for_each = { for i, item in var.forwards : i => item }

    gateway_id = data.scaleway_vpc_public_gateway.main.id
    private_ip = var.lan_ip
    private_port = each.value["lan_port"]
    public_port = each.value["wan_port"]
    protocol = each.value["protocol"]
    depends_on = [scaleway_vpc_public_gateway_dhcp_reservation.main]
}

resource "null_resource" "ufw_status" {
  count = (var.state != "stopped" && length(var.lan_ip) > 0) ? 1 : 0

  triggers = {
    ssh_status = jsonencode(local.ufw_ssh)
    app_status = jsonencode(local.ufw_commands)
  }

  provisioner "remote-exec" {
    inline = concat(
      ["ufw --force reset"],
      local.ufw_ssh,
      local.ufw_commands,
      ["ufw --force enable"]
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

  depends_on = [scaleway_vpc_public_gateway_dhcp_reservation.main]
}

