# Detecting intrusion with canary tokens

## What is a canary token

A canary token is a resource that is monitored for access or tampering. Usually, canary tokens come in the form of a URL, file, API key, or email, etc., and trigger alerts whenever someone (presumably an attacker) trips over them.

## How to detect compromised developer and DevOps environments with canary tokens

Canary tokens can be created and deployed in your code repositories, CI/CD pipelines, project management and ticketing systems like Jira or even instant messaging tools like Slack. When triggered, canary tokens can help alert you of an intrusion in your developer environments.

# Project description

The purpose of the ggcanary project is to provide you with a simple Terraform configuration to create and manage GitGuardian Canary Tokens. We chose to focus on AWS credentials as it is one of the most seeked secret by hackers. It can be found and deployed in multiple places of the SDLC: in source code, in docker containers, as secrets variable in various CI. If a hacker breach your software development toolchain, its first action will be to look for secrets and especially AWS credentials.

Deploying this project will:

- create AWS credentials for their use as GitGuardian Canary Tokens. The users associated with these credentials do not have any permissions, so they cannot perform any action.
- create the related AWS infrastructure required to store any activities related to these credentials with [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) and [AWS S3](https://aws.amazon.com/s3/).
- create the related AWS infrastructure required to send alerts when one of the tokens is tampered to different integration such as email, native webhook and Slack. 

# Project setup

## Requirements

To use this project, you will need:

- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- An [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/). We recommend using an account dedicated to GitGuardian Canary Tokens to avoid all possible security issues.
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [jq](https://stedolan.github.io/jq/) (usually available through your package manager)

## Setup

The main steps to set up the project are the following:

1. [Create an AWS user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) in your account:
   - Give it [sufficient rights to perform its task](./docs/deploy_user_rights.md).
   - Create an access key for that user, that you will use in the next step.
2. Configure your AWS profile for the project. You can run `aws configure --profile YOUR_AWS_ACCOUNT`
3. Setup the [Terraform backend](https://www.terraform.io/language/settings/backends/configuration): fill `backend.tf` with appropriate values
4. Fill a `terraform.tfvars` file that will contain the configuration of the project (AWS profile to use and notifiers to activate):
   - Examples can be found in [`examples/tf_vars`](./examples/tf_vars).
   - See also the [variables reference](./docs/variables_reference.md).
   - Be sure to provide a unique value for `global_prefix`, to avoid name collisions (especially, AWS S3 bucket names have to be unique across all AWS accounts).
5. Create ggcanaries in `ggcanaries.auto.tfvars`
6. If needed, create the S3 bucket and DynamoDB to store the main project state. We provide the `tf_backend` project to do so:
   1. In the `tf_backend` directory, run `terraform init`
   2. In the same directory, run `terraform apply -var-file="../terraform.tfvars"`
7. Run `./scripts/check_setup.sh` to check that you have all the required dependencies, and that you have correctly setup the project
8. Run `terraform init`
9. Run `terraform apply` (this will create all resources for the ggcanaries)
10. ggcanary tokens can be listed using `./scripts/list_keys.sh`

# How-tos

## Use your project

We provide some scripts to help you manage your project once you have deployed it:

### Test the project

Run `./scripts/ggcanary_call.sh <GGCANARY_NAME>` (e.g. `ggtoken1` in the example [below](#mange-your-ggcanaries)) to perform an AWS call with one of the created GitGuardian Canary Tokens. It will try to list S3 buckets with the given ggcanary and send you a notification since one of the ggcanary tokens was used to perform the call.

The script should return the following AWS error message:

> An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied

### List created keys

Run `./scripts/list_keys.sh` to output the list of created keys (secret keys will be displayed as well, be sure to be in a safe environment).

### Display the keys of a given ggcanary

In order to display the keys of a given ggcanary `<GGCANARY_NAME>` from the command line, run `./scripts/display_ggcanary_credentials.sh <GGCANARY_NAME>`.

## Configure your notifications

GitGuardian Canary Tokens support several notification backends such as Amazon SES, Slack, or SendGrid.

The notification backends use the variables defined in the `terraform.tfvars` values for the configuration.
Examples can be found in [`tf vars examples`](./examples/tfvars).

It is possible to add custom notification backend following [this procedure](./docs/how_to_add_a_notifier.md).

## Manage your ggcanaries

In the sample configuration, ggcanaries are specified with the following block:

```
users = {
  ggtoken1 = {
    tag_1 = "John Doe"
    source = "email"
  },
  ggtoken2 = {}
}
```

It will create the ggcanaries:

- `ggtoken1` with tags `{"tag_1": "John Doe", "source": "email"}`
- `ggtoken2` with no tags

### Add a new ggcanary

To add a new ggcanary, you will need to modify the list of ggcanaries. For example, to create a third ggcanary `ggtoken3`, change the value of the `users` block in `ggcanaries.auto.tfvars` to

```
users = {
  ggtoken1 = {
    tag_1 = "John Doe"
    source = "email"
  }
  ggtoken2 = {},
  ggtoken3 = {
    some_other_key = "some_other_value"
  }
}
```

Then run `terraform apply`.

### Remove a ggcanary

To remove a ggcanary, delete it in the `ggcanaries.auto.tfvars` and run `terraform apply`. For example, to remove ggcanary `ggtoken1` from the test configuration, change the value of the `users` block in `ggcanaries.auto.tfvars` to

```
users = {
  ggtoken2 = {}
}
```

Then run `terraform apply`.

### Delete the project

1. Run `terraform destroy` in the main directory.
2. Delete the S3 bucket holding the state (Terraform cannot destroy it for safety reasons).
3. Run `terraform destroy -var-file="../terraform.tfvars"` in the `tf_backend` directory.

# Limitations

## Number of ggcanaries

The number of ggcanaries is limited to 5000 (max number of users linked to an AWS account).

## Number of tags

Each ggcanary can have at most 30 tags. The tag names can be different for each ggcanary.
