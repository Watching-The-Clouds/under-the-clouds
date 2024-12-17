terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.68.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-2"
}

terraform {
    backend "s3" {
    bucket  = "wtc-backend"
    key     = "terraform.tfstate"
    region  = "eu-west-2"
    }
}