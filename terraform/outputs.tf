output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_name" {
    value = module.eks.cluster_name
}

output "vpc-id" {
  value = module.vpc.vpc-id
}

output "oidc-issuer" {
  value = module.eks.cluster_name.identity[0].oidc[0].list
}