/*
 * Tag created resources.
 */
locals {
  tags = {
    "aws-infrastructure/examples/documentdb": ""
  }
}

/*
 * Multi-zone VPC in which to create our deployment.
 *
 * us-east-1e does not support t3.medium, so we exclude it here.
 */
module "vpc" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/vpc_simple"

  availability_zones = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c",
    "us-east-1d",
    "us-east-1f",
  ]

  tags = local.tags
}
