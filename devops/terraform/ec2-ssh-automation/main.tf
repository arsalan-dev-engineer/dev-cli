
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.96.0"
    }
  }
  backend "s3" {
        bucket = "arsalan-s3-bucket-devops"
        key = "arsalan-keypair-devops"
        region = "eu-west-2"
        encrypt = true
    }
}

provider "aws" {
  region = "eu-west-2"
}