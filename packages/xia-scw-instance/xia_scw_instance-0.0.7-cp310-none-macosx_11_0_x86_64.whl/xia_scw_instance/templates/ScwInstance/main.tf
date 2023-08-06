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
