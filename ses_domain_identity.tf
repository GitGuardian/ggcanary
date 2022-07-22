# We only want to apply this configuration when output_SES is active

locals {
  domain_name = (
    var.SES_notifier.enabled
    ? regex(".*@(?P<domain>.*)", var.SES_notifier.parameters.SOURCE_EMAIL_ADDRESS).domain
    : ""
  )
}

resource "aws_route53_record" "domain" {
  zone_id = var.SES_notifier.parameters.zone_id
  name    = local.domain_name
  type    = "TXT"
  ttl     = "60"
  records = [
    aws_ses_domain_identity.domain_identity[0].verification_token
  ]
  count = var.SES_notifier.enabled ? 1 : 0
}

resource "aws_ses_domain_identity" "domain_identity" {
  domain = local.domain_name
  count  = var.SES_notifier.enabled ? 1 : 0
}


resource "aws_ses_domain_identity_verification" "domain_verification" {
  domain     = aws_ses_domain_identity.domain_identity[0].id
  depends_on = [aws_route53_record.domain]
  count      = var.SES_notifier.enabled ? 1 : 0
}
