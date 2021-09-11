/*
 * Tag created resources.
 */
locals {
  tags = {
    "scope-aws-infrastructure/terraform_ecr": ""
  }
}

/*
 * Instance of ECR Simple.
 */
module "ecr" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/ecr_simple"

  names = [
    "scope_aws_infrastructure/scope_web",
    "scope_aws_infrastructure/scope_app"
  ]
}
