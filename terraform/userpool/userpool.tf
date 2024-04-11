resource "aws_ses_configuration_set" "account_recovery" {
  name = "account-recovery"

  reputation_metrics_enabled = true
}

resource "aws_cognito_user_pool" "userpool" {
  name = "uwscope"

  # Protect against deletion
  lifecycle {
    prevent_destroy = true
  }
  deletion_protection = "ACTIVE"

  # Require a username,
  # as allowing "email" or "phone_number" means those must be unique
  alias_attributes = ["preferred_username"]

  # Do not allow self signup, this ensures all accounts are consented participants
  admin_create_user_config {
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

  # Prioritize password resets via email,
  # also specifying this disables legacy SMS / MFA issues.
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  email_configuration {
    configuration_set      = aws_ses_configuration_set.account_recovery.id
    email_sending_account  = "DEVELOPER"
    from_email_address     = "SCOPE Password Reset <do-not-reply@uwscope.org>"
    reply_to_email_address = "do-not-reply@uwscope.org"
    source_arn             = var.ses_domain_identity_arn
  }

  lambda_config {
    custom_message = aws_lambda_function.userpool_custom_message.arn
  }
}

resource "aws_cognito_user_pool_client" "userpool_client" {
  name = "uwscope_client"
  user_pool_id = aws_cognito_user_pool.userpool.id

  generate_secret = false
}
