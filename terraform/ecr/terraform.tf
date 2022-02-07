/*
 * Instance of ECR Simple.
 */
module "ecr" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/ecr"

  names = [
    "uwscope/server_flask",
    "uwscope/web_patient",
    "uwscope/web_registry",
  ]
}
