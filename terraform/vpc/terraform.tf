/*
 * Multi-zone VPC in which to create our deployment.
 *
 * us-east-1e does not support t3.medium, so we currently exclude it.
 * TODO: As our preferred instance type is defined, revisit that decision.
 */
module "vpc" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/vpc"

  availability_zones = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c",
    "us-east-1d",
    "us-east-1f",
  ]

  tags = local.tags
}
