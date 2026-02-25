locals {
  oidc-issuer = module.eks.cluster_name.identity[0].oidc[0].list
}

variable "bucket" {
  type = string
  default = "qrcode-rohit-kalyan"
}
