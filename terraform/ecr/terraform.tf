/*
 * Instance of ECR Simple.
 */
module "ecr" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/ecr"

  names = [
    "scope_aws_infrastructure/scope_web",
    "scope_aws_infrastructure/scope_app"
  ]
}
