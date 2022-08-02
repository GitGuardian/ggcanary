terraform {
  backend "s3" {
    profile        = "938984244085" # Use same value as in tfvars
    region         = "us-west-2" # Use same value as in tfvars
    bucket         = "938984244085-mzhang-bucket" # Use same value as in tfvars
    key            = "terraform.tfstate"
    dynamodb_table = "ggcanary-state-lock"
  }
}
