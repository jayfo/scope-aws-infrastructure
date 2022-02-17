/*
 * CodeBuild for our server_flask Docker image.
 */
module "codebuild" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/codebuild"

  name = "uwscope_web_registry"
  source_archive = var.source_archive
}
