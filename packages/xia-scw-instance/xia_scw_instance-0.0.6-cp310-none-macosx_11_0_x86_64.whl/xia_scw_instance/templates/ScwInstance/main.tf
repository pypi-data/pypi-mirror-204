resource "scaleway_instance_server" "instance" {
  name = var.name
  type = var.type
  image = var.image
  tags = var.tags
}
