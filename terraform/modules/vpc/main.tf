resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = merge(
    {
        Name = "${var.project_name}-vpc"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    }
  )
}

resource "aws_subnet" "private_subnets" {
  vpc_id     = aws_vpc.main.id
  count = length(var.private_subnets)
  cidr_block = var.private_subnets[count.index]
  availability_zone = var.azs[count.index]

  tags = merge(
    {
        Name = "${var.project_name}-private-subn-${var.azs[count.index]}"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/internal-elb" = "1"
    }
  )
}

resource "aws_subnet" "public_subnets" {
  vpc_id     = aws_vpc.main.id
  count = length(var.public_subnets)
  cidr_block = var.public_subnets[count.index]
  availability_zone = var.azs[count.index]

  map_public_ip_on_launch = true

  tags = merge(
    {
        Name = "${var.project_name}-public-subn-${var.azs[count.index]}"
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/internal-elb" = "1"
    }
  )
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.project_name}-public-subn-route-table"
  }
}

resource "aws_route_table_association" "public-subnet-rta" {
  route_table_id = aws_route_table.public-rt.id
  count = length(var.public_subnets)
  subnet_id = aws_subnet.public_subnets[count.index].id
}

resource "aws_eip" "nat-eip" {
  domain   = "vpc"

  depends_on = [ aws_internet_gateway.igw ]
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat-eip.id

  subnet_id     = aws_subnet.public_subnets[0].id

  tags = {
    Name = "gw NAT"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.igw]
}

resource "aws_route_table" "private-rt" {
  vpc_id = aws_vpc.main.id

  count = length(var.private_subnets)

  tags = {
    Name = "${var.project_name}-private-rt-${count.index}"
 
 }
}

resource "aws_route" "r" {
  count = length(var.private_subnets)
  route_table_id            = aws_route_table.private-rt[count.index].id
  destination_cidr_block    = "0.0.0.0/0"
  nat_gateway_id = aws_nat_gateway.nat.id
}

resource "aws_route_table_association" "private-rta" {
  count = length(var.private_subnets)
  route_table_id = aws_route_table.private-rt[count.index].id 
  subnet_id = aws_route_table.private-rt[count.index].id
}