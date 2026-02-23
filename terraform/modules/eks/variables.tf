variable "cluster_name" {
  type = string
  description = "Cluster Name"
}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  description = "VPC id"
  type = string
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
}

variable "eks_version" {
  type = string
  description = "Version of Kubernetes"
}
