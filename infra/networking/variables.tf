#------networking/variables.tf

variable "vpc_cidr" {}

variable "public_cidrs" {
  type = list(string)
}

variable "accessip" {}
variable "jumpboxip" {}

variable "private_cidrs" {
  type = list(string)
}