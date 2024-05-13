resource "aws_lambda_function" "cost_notification_lambda" {
  function_name = "cost-notification-lambda"
  runtime       = "python3.8"
  handler       = "lambda_function.lambda_handler"
  s3_bucket     = aws_s3_bucket.lambda_bucket.bucket
  s3_key        = aws_s3_object.lambda_object.key
  role          = aws_iam_role.lambda_role.arn
}