/*
 * CodeBuild for scope_web.
 */
module "codebuild_scope_web" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/codebuild"

  name = "scope_web"
}

/*
 * CodeBuild for scope_app.
 */
module "codebuild_scope_app" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/codebuild"

  name = "scope_app"
}
