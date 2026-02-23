terraform {
  backend "s3" {
    region = "us-east-1"
    bucket = "rohit-kandulapati-terraform-projects"
    key = "devops-qrcode/terraform.tfstate"
    use_lockfile = true
    encrypt = true
  }
}