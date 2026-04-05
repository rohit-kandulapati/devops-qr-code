data "terraform_remote_state" "eks" {
  backend = "s3"

  config = {
    bucket = "rohit-kandulapati-terraform-projects"
    key = "devops-qrcode/terraform.tfstate"
    region = "us-east-1"
  }
}

locals {
  oidc_issuer = replace(data.terraform_remote_state.eks.outputs.oidc_issuer, "https://", "")
}
#data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer

# data "aws_eks_cluster" "cluster" {
#   name = output.cluster_name
# }

data "tls_certificate" "oidc" { # tls_certificate fetches the TLS cert(s) presented by that URL
  url = data.terraform_remote_state.eks.outputs.oidc_issuer
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
