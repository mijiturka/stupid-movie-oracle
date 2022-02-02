variable "region" {
  default = "eu-west"
}

variable "api_token" {
  sensitive = true
}

variable "ssh_user" {
  sensitive = true
}
variable "root_user_pwd" {
  sensitive = true
}
