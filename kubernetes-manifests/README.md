## Testing in local KIND cluster
For testing in local kind cluster create a new secret.yaml with the AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY to use them in your python image.

These are manifests are only helpful for testing in local kind cluster, if you want to use them in EKS or any managed kubernetes services, you should use write a manifest for alb ingress respective to the cloud provider for external access.

In local kind cluster, port forward the frontend-nextjs for testing. And it is working absolutely fine.