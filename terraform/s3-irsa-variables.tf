locals {
  oidc_issuer = replace(data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer, "https://", "")
}


data "aws_eks_cluster" "cluster" {
  name = var.cluster_name
}

data "tls_certificate" "oidc" { # tls_certificate fetches the TLS cert(s) presented by that URL
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