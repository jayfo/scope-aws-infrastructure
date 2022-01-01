resource "aws_cognito_user_pool" "userpool" {
  name = "uwscope"

  alias_attributes = ["email", "phone_number", "preferred_username"]

  admin_create_user_config {
    # Do not allow self signup, this ensures all accounts are consented participants
    allow_admin_create_user_only = true
  }

  # TODO: MFA requires SMS

  # TODO: Require verification of email?

  # mfa_configuration = "OPTIONAL"

}

resource "aws_cognito_user_pool_client" "userpool_client" {
  name = "uwscope_client"
  user_pool_id = aws_cognito_user_pool.userpool.id

  generate_secret = false
}
