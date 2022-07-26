provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.9.0"
    }
  }

  required_version = ">= 0.14.9"

  # No remote backend
}

# terraform state file setup
# create an S3 bucket to store the state file in
resource "aws_s3_bucket" "terraform-states-storage" {
  bucket = var.backend_s3_bucket
  tags = {
    Name = "S3 Remote Terraform States Store"
    Role = "backend"
  }
}
resource "aws_s3_bucket_versioning" "terraform-states-storage" {
  bucket = aws_s3_bucket.terraform-states-storage.id
  versioning_configuration {
    status = "Enabled"
  }
}
resource "aws_s3_bucket_public_access_block" "terraform-states-storage" {
  bucket = aws_s3_bucket.terraform-states-storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform-states-storage" {
  bucket = aws_s3_bucket.terraform-states-storage.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_dynamodb_table" "dynamodb-terraform-state-lock" {
  name           = "ggcanary-state-lock"
  hash_key       = "LockID"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "DynamoDB Terraform States Lock Table"
    Role = "locking"
  }
}
