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
  value = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
}

output "s3-iam-role-arn" {
  value = aws_iam_role.s3-role.arn
}