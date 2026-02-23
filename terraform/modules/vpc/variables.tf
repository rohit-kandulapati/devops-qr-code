variable "vpc_cidr" {
  type = string
  description = "CIDR Block of your VPC"
}

variable "project_name" {
  type = string
  description = "Name of this project"
}

variable "cluster_name" {
  type = string
  description = "Name of the cluster"
}

variable "private_subnets" {
    type = list(string)
    description = "List of your private sunet cidrs"
}

variable "public_subnets" {
  type = list(string)
  description = "List of your public subnet cidrs"
}

variable "azs" {
  type = list(string)
  description = "List of you AZs"
}


