## DevOps-QR-Code
We should attach an IAM Role, using IRSA for the python pod to access the s3 bucket.
1. Create that role.
2. Create an SA
3. Attach that service account to the pod

## CORS
The cors issues - commented the cors middleware section. 
- Re-build the images and test in local kind.
- Push them if they are working to dockerhub.
- Remove the accesskeys as envs in yaml manifests 


aws eks update-kubeconfig --name qrcode --region us-east-1

[AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)

## Ingress Controller using Helm
[Ingress Controller](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html)
```Bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.14.1/docs/install/iam_policy.json

aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
    --cluster=<cluster-name> \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --region <aws-region-code> \
    --approve

helm repo add eks https://aws.github.io/eks-charts

helm repo update eks

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --version 1.14.0
```

## Tools Installation
```Bash
## Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

## aws cli installation
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```