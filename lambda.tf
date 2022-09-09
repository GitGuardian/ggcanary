locals {
  lambda_function_name   = "${var.global_prefix}-lambda"
  lambda_parameters_file = "builds/ggcanary_lambda_parameters.json"
}


resource "local_sensitive_file" "notifier_parameters" {
  content         = jsonencode(local.ggcanary_lambda_parameters)
  filename        = local.lambda_parameters_file
  file_permission = "0600"
}



module "lambda_function" {

  source  = "terraform-aws-modules/lambda/aws"
  version = "3.2.0"
  depends_on = [
    local_sensitive_file.notifier_parameters
  ]

  source_path = [
    {
      path             = "lambda/entrypoint.py",
      pip_requirements = "lambda/requirements.txt"
    },
    {
      path          = "lambda/lambda_py",
      prefix_in_zip = "lambda_py",
    },
    {
      path     = "."
      patterns = ["!.*", local.lambda_parameters_file]
    }
  ]
  function_name = local.lambda_function_name
  handler       = "entrypoint.lambda_handler"
  runtime       = "python3.8"
  publish       = true

  environment_variables = {
    GGCANARY_USER_PREFIX = var.global_prefix,
  }


  allowed_triggers = {
    AllowExecutionFromS3Bucket = {
      service    = "s3"
      source_arn = aws_s3_bucket.ggcanary_bucket.arn
    }
  }

  assume_role_policy_statements = {
    assume_role = {
      effect  = "Allow"
      actions = ["sts:AssumeRole"]
      principals = {
        account_principals = {
          type        = "Service"
          identifiers = ["lambda.amazonaws.com"]
        }
      }
    }
  }

  cloudwatch_logs_retention_in_days = 90
  attach_cloudwatch_logs_policy     = true
  attach_policy_statements          = true
  policy_statements = {
    get_object = {
      effect    = "Allow"
      actions   = ["s3:GetObject"]
      resources = ["arn:aws:s3:::${aws_s3_bucket.ggcanary_bucket.bucket}/ggcanary/*"]
    }
    list_user_tags = {
      effect = "Allow"
      actions = [
        "iam:ListUserTags",
      ]
      resources = ["arn:aws:iam::${data.aws_caller_identity.current.id}:user/ggcanary/*"]
    }
    ses_send_email = {
      effect = "Allow"
      actions = [
        "ses:SendEmail",
        "ses:SendRawEmail"
      ]
      resources = ["arn:aws:ses:*:${data.aws_caller_identity.current.id}:identity/*"]
    }
  }
}


resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.ggcanary_bucket.id

  lambda_function {
    lambda_function_arn = module.lambda_function.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "ggcanary/AWSLogs/"
    filter_suffix       = ".json.gz"
  }
  depends_on = [module.lambda_function]

}

resource "null_resource" "remove_temp_file" {
  provisioner "local-exec" {
    command = "rm -f ${local.lambda_parameters_file}"
  }
  depends_on = [module.lambda_function]
  triggers = {
    always_run = timestamp()
  }
}
