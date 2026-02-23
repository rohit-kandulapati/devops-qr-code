output "vpc-id" {
  value = aws_vpc.main.id
}

output "private-subnet-ids" {
  value = aws_subnet.private_subnets[*].id
}

output "public-subnet-ids" {
    value = aws_subnet.public_subnets[*].id 
}

output "igw-id" {
    value = aws_internet_gateway.igw.id
}

output "nat-id" {
    value = aws_nat_gateway.nat[*].id
}