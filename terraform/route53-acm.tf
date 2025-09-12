resource "aws_route53_zone" "main" {
  name = "pwc-task.com"
}

resource "aws_acm_certificate" "main" {
  domain_name       = "pwc-task.com"
  validation_method = "DNS"
  subject_alternative_names = [
    "prometheus.pwc-task.com",
    "grafana.pwc-task.com"
  ]
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      type   = dvo.resource_record_type
      record = dvo.resource_record_value
    }
  }
  zone_id = aws_route53_zone.main.zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
