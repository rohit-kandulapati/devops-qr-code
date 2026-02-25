locals {
  oidc_issuer = replace(data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer, "https://", "")
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
}

data "aws_iam_openid_connect_provider" "oidc_arn" {
  url = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
}

variable "bucket" {
  type = string
  default = "qrcode-rohit-kalyan"
}

variable "namespace" {
  type = string
  default = "default"
}

variable "sa_name" {
  type = string
  default = "s3-getput"
}