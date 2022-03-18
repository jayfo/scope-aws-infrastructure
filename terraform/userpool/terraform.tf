resource "aws_cognito_user_pool" "userpool" {
  name = "uwscope"

  lifecycle {
    prevent_destroy = true
  }

  # Require a username,
  # as allowing "email" or "phone_number" means those must be unique
  alias_attributes = ["preferred_username"]

  admin_create_user_config {
    # Do not allow self signup, this ensures all accounts are consented participants
    allow_admin_create_user_only = true
  }

  password_policy {
    # Password generated at account creation is good for 90 days
    temporary_password_validity_days = 90

    # These are the defaults
    minimum_length = 8
    require_lowercase = true
    require_numbers = true
    require_symbols = true
    require_uppercase = true
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
