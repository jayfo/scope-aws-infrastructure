/*
 * Tag created resources.
 */
locals {
  tags = {
    "scope-aws-infrastructure/terraform_eip": ""
  }
}

/*
 * An elastic IP.
 */
resource "aws_eip" "eip" {
  tags = local.tags
}
