/*
 * Zone with DNS records.
 */
module "hosted_zone" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/hosted_zone"

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
    {
      name = "app.demo.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "registry.demo.uwscope.org",
      ip = var.eip_public_ip,
    },

    /* Dev Deployment */
    {
      name = "dev.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "registry.dev.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "app.dev.uwscope.org",
      ip = var.eip_public_ip,
    },

    /* Multicare Deployment */
    {
      name = "multicare.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "app.multicare.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "registry.multicare.uwscope.org",
      ip = var.eip_public_ip,
    },

    /* SCCA Deployment */
    {
      name = "scca.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "app.scca.uwscope.org",
      ip = var.eip_public_ip,
    },
    {
      name = "registry.scca.uwscope.org",
      ip = var.eip_public_ip,
    },
  ]

  tags = local.tags
}
