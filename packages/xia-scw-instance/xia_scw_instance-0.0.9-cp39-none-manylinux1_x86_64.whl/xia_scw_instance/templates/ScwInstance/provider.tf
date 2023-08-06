terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  zone   = "fr-par-1"
  region = "fr-par"
  access_key = "{{ access_key }}"
  secret_key = "{{ secret_key }}"
  organization_id = "{{ organization_id }}"
  project_id = "{{ project_id }}"
}
