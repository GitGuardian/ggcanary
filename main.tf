terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9.0"
    }
  }
  required_version = ">= 0.14.9"

}


provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}
