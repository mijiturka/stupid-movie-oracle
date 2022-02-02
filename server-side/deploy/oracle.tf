terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "1.25.2"
    }
  }
}

provider "linode" {
  token = var.api_token
}

resource "linode_instance" "mayonesia-oracle" {
  image   = "linode/debian10"
  label   = "mayonesia-oracle"
  group   = "mayonesia"
  region  = var.region
  type    = "g6-nanode-1"
  backups_enabled = false
  authorized_users  = [ var.ssh_user ]
  root_pass         = var.root_user_pwd
}

output "ip" {
  value = linode_instance.mayonesia-oracle.ip_address
}
