/*
 * Explicit configuration of providers.
 */
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.9.0"
    }
  }
}

locals {
  domain_name = "uwscope.org"
}

/*
 * Zone for managing our DNS.
 */
resource "aws_route53_zone" "dns_zone" {
  name = local.domain_name
}

/*
 * Whenever the zone is created, or its name servers are otherwise modified,
 * update the domain to point and the name servers for the zone.
 *
 * https://github.com/hashicorp/terraform-provider-aws/issues/88
 */
resource "null_resource" "aws_domain_com_nameservers" {
  triggers = {
    nameservers = join(", ",sort(aws_route53_zone.dns_zone.name_servers))
  }

  provisioner "local-exec" {
    command = "aws route53domains update-domain-nameservers --domain-name ${local.domain_name} --nameservers ${join(" ",formatlist(" Name=%s",sort(aws_route53_zone.dns_zone.name_servers)))}"
  }
}

/*
 * Record for "uwscope.org"
 */
resource "aws_route53_record" "root_dns" {
  zone_id = aws_route53_zone.dns_zone.zone_id

  name = "uwscope.org"
  type = "A"
  ttl = "15"

  records = [var.eip_public_ip]
}

/*
 * Record for "www.uwscope.org"
 */
resource "aws_route53_record" "www_dns" {
  zone_id = aws_route53_zone.dns_zone.zone_id

  name = "www.uwscope.org"
  type = "A"
  ttl = "15"

  records = [var.eip_public_ip]
}
