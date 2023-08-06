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
  value = scaleway_instance_server.instance.image
}

output "state" {
  value = scaleway_instance_server.instance.state
}

output "tags" {
  value = scaleway_instance_server.instance.tags
}
