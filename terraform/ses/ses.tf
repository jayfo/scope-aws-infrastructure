resource "aws_ses_domain_identity" "uwscope_org" {
  domain = "uwscope.org"
}

resource "aws_ses_domain_dkim" "uwscope_org" {
  domain = aws_ses_domain_identity.uwscope_org.domain
}

resource "aws_ses_domain_mail_from" "uwscope_org" {
  domain           = aws_ses_domain_identity.uwscope_org.domain
  mail_from_domain = "bounce.${aws_ses_domain_identity.uwscope_org.domain}"
}
