# Variables

This terraform can be configured with the following variables:

| Variable name       |               | Description.                                                                            |
| ------------------- | ------------- | --------------------------------------------------------------------------------------- |
| `aws_profile`       | **mandatory** | AWS profile to use to deploy the project. The profile should have sufficient rigths.    |
| `s3_bucket`         | **Optional**  | Name of the S3 bucket holding the state. Mandatory to configure with `tf_backend`       |
| `aws_region`        | **mandatory** | AWS region where the project will be deployed.                                          |
| `global_prefix`     | **mandatory** | Prefix that will be used to generate unique name for resources, especially for buckets. |
| `users`             | Optional      | GGCanary tokens to create.                                                              |
| `SES_notifier`      | Optional      | Configuration of the SES Notifier.                                                      |
| `Slack_notifier`    | Optional      | Configuration of the Slack Notifier.                                                    |
| `SendGrid_notifier` | Optional      | Configuration of the SendGrid Notifier.                                                 |

See examples in [`examples/tf_vars`](/examples/tf_vars)
