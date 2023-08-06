output "project_id" {
  value = var.project_id
}

output "name" {
  value = scaleway_instance_server.instance.name
}

output "type" {
  value = scaleway_instance_server.instance.type
}

output "image" {
  value = data.scaleway_instance_image.my_image.name
}

output "state" {
  value = scaleway_instance_server.instance.state
}

output "tags" {
  value = scaleway_instance_server.instance.tags
}

output "vpc_name" {
  value = var.vpc_name
}

output "wan_ip" {
  value = var.wan_ip
}

output "lan_ip" {
  value = var.lan_ip
}

output "lan_name" {
  value = var.lan_name
}

output "ssh_hosts" {
  value = var.ssh_hosts
}

output "forwards" {
  value = var.forwards
}

output "ufw_rules" {
  value = local.ufw_commands
}

output "ssh_rules" {
  value = local.ufw_ssh
}