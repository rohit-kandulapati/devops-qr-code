output "oidc_issuer" {
  value = data.terraform_remote_state.eks.outputs.oidc_issuer
}

output "s3-iam-role-arn" {
  value = aws_iam_role.s3-role.arn
}