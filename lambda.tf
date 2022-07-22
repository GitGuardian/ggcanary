locals {
  lambda_function_name = "${var.global_prefix}-lambda"
}

resource "null_resource" "generate_requirements" {
  triggers = {
    lockfile_sha1 = "${sha1(file("lambda/Pipfile.lock"))}"
    script_sha1   = "${sha1(file("lambda.tf"))}"
    target        = "/tmp/tf-lambda-requirements.txt"
  }

  provisioner "local-exec" {
    command     = "pipenv run pipfile2req | grep -v botocore | grep -v boto3 | grep -v s3transfer > /tmp/tf-lambda-requirements.txt"
    working_dir = "lambda"
  }
}

locals {
  enabled_notifiers = join(",", [
    for value in local.notifiers : upper(value.name)
    if value.enabled
  ])
  parameters_map_list = tolist([
    for value in local.notifiers : {
      for param_name, param_value in value.parameters :
      "${upper(value.name)}_${param_name}" => param_value
    }
    if value.enabled
  ])

  parameters_map = merge(local.parameters_map_list...)
}


module "lambda_function" {

  source     = "terraform-aws-modules/lambda/aws"
  version    = "3.2.0"
  depends_on = [null_resource.generate_requirements]

  source_path = [
    {
      path             = "lambda/entrypoint.py",
      pip_requirements = "/tmp/tf-lambda-requirements.txt"
    },
    {
      path          = "lambda/lambda_py",
      prefix_in_zip = "lambda_py",
    }
  ]
  function_name = local.lambda_function_name
  handler       = "entrypoint.lambda_handler"
  runtime       = "python3.8"
  publish       = true

  environment_variables = merge(
    {
      GGCANARY_USER_PREFIX = var.global_prefix,
      ENABLED_NOTIFIERS    = local.enabled_notifiers
    },
    local.parameters_map
  )

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

  attach_cloudwatch_logs_policy = true
  attach_policy_statements      = true
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

}
