
variable "aws_profile" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "terraform_backend_s3_bucket" {
  description = "S3 bucket name for terraform state"
  type        = string
}

variable "global_prefix" {
  type = string
}

variable "users" {
  type    = map(map(string))
  default = {}
}

variable "SES_notifiers" {
  type = list(object({
    zone_id              = string
    source_email_address = string
    dest_email_address   = string
  }))
  default = []
}

variable "Slack_notifiers" {
  type = list(object({
    webhook = string
  }))
  default = []
}

variable "SendGrid_notifiers" {
  type = list(object({
    api_key              = string
    source_email_address = string
    dest_email_addresses = list(string)
  }))
  default = []
}


locals {
  ggcanary_lambda_parameters = concat(
    [
      for notifier_config in var.SES_notifiers :
      {
        kind       = "ses"
        parameters = notifier_config
      }
    ],
    [
      for notifier_config in var.Slack_notifiers :
      {
        kind       = "slack"
        parameters = notifier_config
      }
    ],
    [
      for notifier_config in var.SendGrid_notifiers :
      {
        kind       = "sendgrid"
        parameters = notifier_config
      }
    ],
  )
}
