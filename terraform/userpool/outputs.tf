/*
 * Cognito user pool.
 */
output "userpool" {
  value = aws_cognito_user_pool.userpool
}

/*
 * Cognito user pool client.
 */
output "userpool_client" {
  value = aws_cognito_user_pool_client.userpool_client
  sensitive = true
}
