
variable "aws_profile" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "users" {
  type    = map(map(string))
  default = {}
}


variable "global_prefix" {
  type = string
}


variable "SES_notifier" {
  type = object({
    enabled = bool
    parameters = object({
      SOURCE_EMAIL_ADDRESS = string
      DEST_EMAIL_ADDRESS   = string
      zone_id              = string
    })
  })
  default = {
    enabled    = false
    parameters = null
  }
}

variable "Slack_notifier" {
  type = object({
    enabled = bool
    parameters = object({
      WEBHOOK = string
    })
  })
  default = {
    enabled    = false
    parameters = null
  }
}

variable "SendGrid_notifier" {
  type = object({
    enabled = bool
    parameters = object({
      API_KEY              = string
      SOURCE_EMAIL_ADDRESS = string
      DEST_EMAIL_ADDRESSES = string
    })
  })
  default = {
    enabled    = false
    parameters = null
  }
}

locals {
  notifiers = [
    {
      name       = "SES"
      enabled    = var.SES_notifier.enabled
      parameters = var.SES_notifier.parameters
    },
    {
      name       = "Slack"
      enabled    = var.Slack_notifier.enabled
      parameters = var.Slack_notifier.parameters
    },
    {
      name       = "SendGrid"
      enabled    = var.SendGrid_notifier.enabled
      parameters = var.SendGrid_notifier.parameters
    },
  ]
}
