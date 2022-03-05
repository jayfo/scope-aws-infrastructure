/*
 * A random password for the admin account.
 */
resource "random_password" "admin_password" {
  length           = 32
  special          = false
}

/*
 * Instance of DocumentDB.
 */
module "documentdb" {
  source = "github.com/fogies/aws-infrastructure//terraform_common/documentdb"

  name = "scope-documentdb"

  apply_immediately = true

  admin_user = "scope_admin"
  admin_password = random_password.admin_password.result

  instance_count = 1
  instance_class = "db.t3.medium"
  subnet_ids = var.subnet_ids

  tags = local.tags
}
