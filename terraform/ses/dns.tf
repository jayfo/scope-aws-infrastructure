resource "aws_route53_record" "identity_verification_uwscope_org" {
  zone_id = var.hosted_zone_id
  name    = "_amazonses.uwscope.org"
  type    = "TXT"
  ttl     = "600"
  records = [aws_ses_domain_identity.uwscope_org.verification_token]
}

resource "aws_route53_record" "dkim_uwscope_org" {
  count   = length(aws_ses_domain_dkim.uwscope_org.dkim_tokens)

  zone_id = var.hosted_zone_id
  name    = format(
    "%s._domainkey.%s",
    element(aws_ses_domain_dkim.uwscope_org.dkim_tokens, count.index),
    "uwscope.org",
  )
  type    = "CNAME"
  ttl     = "600"
  records = ["${element(aws_ses_domain_dkim.uwscope_org.dkim_tokens, count.index)}.dkim.amazonses.com"]
}

resource "aws_route53_record" "domain_mail_from_mx_uwscope_org" {
  zone_id = var.hosted_zone_id
  name    = aws_ses_domain_mail_from.uwscope_org.mail_from_domain
  type    = "MX"
  ttl     = "600"
  records = ["10 feedback-smtp.us-east-1.amazonses.com"]
}

resource "aws_route53_record" "domain_mail_from_txt_uwscope_org" {
  zone_id = var.hosted_zone_id
  name    = aws_ses_domain_mail_from.uwscope_org.mail_from_domain
  type    = "TXT"
  ttl     = "600"
  records = ["v=spf1 include:amazonses.com -all"]
}
