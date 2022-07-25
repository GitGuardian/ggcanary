# Project description

The purpose of this project is to have a Terraform configuration that allows the creation of GitGuardian Canary Tokens.

Deploying this project will

- create credentials that can be used as GitGuardian Canary Tokens. The users associated with these credentials do not have any permission, so they cannot perform any action.
- create AWS entities required to send alerts when one of these token is used.

# Project setup

## Requirements

In order to use this project, you will need:

- [terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- An [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/). Note that we recommend using an account dedicated to GitGuardian Canary Tokens, to avoid all possible security issues.
- [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [jq](https://stedolan.github.io/jq/) (usually available through your package manager)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

## Setup

The main steps to setup the project are the following:

1. Configure your AWS profile for the project. You can run `aws configure --profile YOUR_AWS_ACCOUNT`.
2. Setup the [Terraform backend](https://www.terraform.io/language/settings/backends/configuration):
   1. Add a `backend.tf.json` declaring a backend (examples can be found in [`examples/backend`](./examples/backend)).
   2. If you use S3 as a backend, run the [`./scripts/configure_s3.sh`](./scripts/configure_s3.sh). This will create the S3 bucket and DynamoDB table to store the terraform state.
3. Fill a `terraform.tfvars` file, that will contain the configuration of the project (AWS profile to use, ggcanary to create, as well as which notifiers to activate):
   - Examples can be found in [`examples/tf_vars`](./examples/tf_vars).
   - See also the [variables reference](./docs/variables_reference.md).
   - Be sure to provide a unique value for `global_prefix`, to avoid name collisions (especially, AWS S3 bucket names have to be unique across all AWS accounts).
4. Run `./scripts/setup.sh` to check that you have all the required dependencies and install the required Python virtualenv.
5. Run `terraform init`.
6. Run `terraform apply`.
7. Ggcanaries can be listed using `./scripts/list_keys.sh`.

# How-tos

## Use your project

We provide some scripts to help you manage your project, once it is deployed:

### Test the project

Run `./scripts/ggcanary_call.sh <GGCANARY_NAME>` (e.g. `ggtoken1` in the example [below](#mange-your-ggcanaries)) to perform an AWS call with one of the created GitGuardian Canary Tokens.
It will try to list S3 buckets with the given ggcanary, and send you a notification, since one of the ggcanary token was used to perform the call.

Please note that it is expected that the script display the following AWS error message:

> An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied

### List created keys

Run `./scripts/list_keys.sh` to output the list of created keys (secret keys will be displayed as well, be sure to be in a safe environment).

### Display the keys of a given ggcanary

In order to display the keys of a given ggcanary `<GGCANARY_NAME>` from the command line, run `./scripts/display_ggcanary_credentials.sh <GGCANARY_NAME>`.

## Configure your notifications

GitGuardian Canary Tokens support several notification backends such as Amazon SES, Slack or SendGrid.

The notification backends use the variables defined in the `terraform.tfvars` values for configuration.
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

This will create the ggcanaries

- `ggtoken1` with tags `{"tag_1": "John Doe", "tag_2": "email"}`
- `ggtoken2` with no tags

### Add a new ggcanary

In order to add a new ggcanary, you will need to modify the list of ggcanaries. For example, to create a third ggcanary `ggtoken3`, change the value of the `users` block in `terraform.tfvars` to

```
users = {
  ggtoken1 = {
    username = "John Doe"
    location = "email"
  }
  ggtoken2 = {},
  ggtoken3 = {
    some_other_key = "some_other_value"
  }
}
```

Then run `terraform apply`.

### Remove a ggcanary

In order to remove a ggcanary, delete it in the `terraform.tfvars` and run `terraform apply`. For example, to remove ggcanary `ggtoken1` from the test configuration, change the value of the `users` block in `terraform.tfvars` to

```
users = {
  ggtoken2 = {}
}
```

Then run `terraform apply`.

# Limitations

## Number of ggcanaries

The number of ggcanaries is limited to 5000 (max number of users linked to an AWS account).

## Number of tags

Each ggcanary can have at most 30 tags. The tag names can be different for each ggcanary.
