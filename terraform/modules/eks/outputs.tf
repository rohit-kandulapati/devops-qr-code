output "cluster_endpoint" {
  value = aws_eks_cluster.eks-cluster.endpoint
}

output "cluster_name" {
  value = aws_eks_cluster.eks-cluster.name
}

output "oidc-issuer" {
  value = aws_eks_cluster.eks-cluster.identity[0].oidc[0].issuer
}