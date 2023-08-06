terraform {
  backend "local" {
    path = "{{ tfstate_path }}"
  }
}