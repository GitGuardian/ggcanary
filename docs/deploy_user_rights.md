We recommand that you use a dedicated AWS user to deploy the project.

The following policy can be associated to the user, so that it has sufficient rights to perform it's task:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": [
        "cloudtrail:*",
        "dynamodb:*",
        "iam:*",
        "lambda:*",
        "logs:*",
        "s3:*"
      ],
      "Resource": "*"
    }
  ]
}
```

Note that if you plan to use the SES Notifier, you would also need those additional rights:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VisualEditor0",
      "Effect": "Allow",
      "Action": ["route53:*", "route53domains:*", "ses:*"],
      "Resource": "*"
    }
  ]
}
```
