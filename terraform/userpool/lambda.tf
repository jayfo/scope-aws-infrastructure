data "archive_file" "lambda_userpool_custom_message" {
    type        = "zip"
    source_dir  = "${path.module}/lambda/"
    output_path = "${path.module}/lambda.zip"
}

data "aws_iam_policy_document" "policy_document_assume_lambda" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "lambda_userpool_custom_message" {
  name = "lambda_userpool_custom_message"

  assume_role_policy = data.aws_iam_policy_document.policy_document_assume_lambda.json
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  ]
}

resource "aws_lambda_function" "userpool_custom_message" {
    filename         = data.archive_file.lambda_userpool_custom_message.output_path
    source_code_hash = data.archive_file.lambda_userpool_custom_message.output_base64sha256
    function_name    = "userpool_custom_message"
    role             = aws_iam_role.lambda_userpool_custom_message.arn
    handler          = "lambda.lambda_handler"
    runtime          = "python3.12"
}

resource "aws_lambda_permission" "allow_cognito" {
  statement_id  = "AllowExecutionFromCognito"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.userpool_custom_message.function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.userpool.arn
}
