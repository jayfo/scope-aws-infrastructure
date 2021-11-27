/*
 * Tag created resources.
 */
locals {
  tags = {
    "scope-aws-infrastructure/terraform_dns": ""
  }
}

/*
 * Zone with DNS records.
 */
module "hosted_zone" {
#  source = "github.com/fogies/aws-infrastructure//terraform_common/hosted_zone"
  source = "github.com/jayfo/aws-infrastructure?ref=aws//terraform_common/hosted_zone"

  name = "uwscope.org"

  address_records = [
    /* Root Domains */
    {
      name = "uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "www.uwscope.org",
      ip = var.eip_public_ip,
    },
    /* Demo Deployment */
    {
      name = "demo.uwscope.org",
      ip = var.eip_public_ip,
    },
    /* Dev Deployment */
    {
      name = "dev.uwscope.org",
      ip = var.eip_public_ip,
    },
  ]

  tags = local.tags
}
