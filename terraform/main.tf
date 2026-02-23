module "vpc" {
  source = "./modules/vpc"

  vpc_cidr = var.vpc_cidr
  project_name = var.project_name
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets
  azs = var.azs
  cluster_name = var.cluster_name
}

module "eks" {
  source = "./modules/eks"

  cluster_name = var.cluster_name
  eks_version = var.eks_version
  vpc_id = module.vpc.vpc-id
  subnet_ids = module.vpc.private-subnet-ids
  node_groups = var.node_groups
}