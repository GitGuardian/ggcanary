# We only want to apply this configuration when output_SES is active

locals {
  zone_ids_with_domain_set = toset([
    for notifier_config in var.SES_notifiers :
    {
      zone_id     = notifier_config.zone_id
      domain_name = regex(".*@(?P<domain>.*)", notifier_config.source_email_address).domain
    }
  ])
  zone_id_to_domain_map = {
    for elem in local.zone_ids_with_domain_set :
    elem.zone_id => elem.domain_name
  }
}

resource "aws_ses_domain_identity" "domain_identity" {
  domain   = each.value
  for_each = local.zone_id_to_domain_map
}


resource "aws_route53_record" "domain" {
  zone_id = each.key
  name    = each.value
  type    = "TXT"
  ttl     = "60"
  records = [
    aws_ses_domain_identity.domain_identity[each.key].verification_token
  ]
  for_each = local.zone_id_to_domain_map
}


resource "aws_ses_domain_identity_verification" "domain_verification" {
  domain     = aws_ses_domain_identity.domain_identity[each.key].id
  depends_on = [aws_route53_record.domain]
  for_each   = local.zone_id_to_domain_map
}
