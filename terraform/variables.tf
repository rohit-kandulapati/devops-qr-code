variable "vpc_cidr" {
  type = string
  default = "10.0.0.0/16"
}

variable "project_name" {
  type = string
  default = "qrcode"
}

variable "cluster_name" {
  type = string
  default = "qrcode"
}

variable "private_subnets" {
  type = list(string)
  default = [ "10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24" ]
}

variable "public_subnets" {
  type = list(string)
  default = [ "10.0.4.0/24" ]
}

variable "azs" {
  type = list(string)
  default = [ "us-east-1a", "us-east-1b", "us-east-1c" ]
}

variable "eks_version" {
  type = string
  default = "1.34"
}

variable "node_groups" {
  description = "EKS node group description"
  type = map(object({
    instance_types = list(string)
    capacity_type = string
    scaling_config = object({
      desired_size = number
      max_size = number
      min_size = number
    }) 
  }))
  default = {
    default_group = {
      instance_types = ["m7i-flex.large"]
      capacity_type = "ON_DEMAND"
      scaling_config = {
        desired_size = 1
        max_size = 3
        min_size = 1
      }
    }
  }
}
