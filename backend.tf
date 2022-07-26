terraform {
  backend "s3" {
    profile        = "CHANGEME" # Use same value as in tfvars
    region         = "CHANGEME" # Use same value as in tfvars
    bucket         = "CHANGEME" # Use same value as in tfvars
    key            = "terraform.tfstate"
    dynamodb_table = "ggcanary-state-lock"
  }
}
