# Variables

This terraform can be configured with the following variables:

## terraform.tfvars

This file holds the configuration for the infrastructure and the notifiers.

| Variable name                 |               | Description.                                                                            |
| ----------------------------- | ------------- | --------------------------------------------------------------------------------------- |
| `aws_profile`                 | **mandatory** | AWS profile to use to deploy the project. The profile should have sufficient rigths.    |
| `terraform_backend_s3_bucket` | **Optional**  | Name of the S3 bucket holding the state. Mandatory to configure with `tf_backend`       |
| `aws_region`                  | **mandatory** | AWS region where the project will be deployed.                                          |
| `global_prefix`               | **mandatory** | Prefix that will be used to generate unique name for resources, especially for buckets. |
| `SES_notifiers`               | Optional      | Configuration of the SES Notifiers.                                                     |
| `Slack_notifiers`             | Optional      | Configuration of the Slack Notifiers.                                                   |
| `SendGrid_notifiers`          | Optional      | Configuration of the SendGrid Notifiers.                                                |

See examples in [`examples/tf_vars`](/examples/tf_vars)

## ggcanaries.auto.tfvars

This file holds the ggcanary to create and monitor.

| Variable name |          | Description.               |
| ------------- | -------- | -------------------------- |
| `users`       | Optional | GGCanary tokens to create. |
