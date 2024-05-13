# Define CloudWatch Events rule to trigger Lambda every 24 hours
resource "aws_cloudwatch_event_rule" "lambda_trigger_rule" {
  name                = "lambda-trigger-rule"
  schedule_expression = "rate(24 hours)"
}

# Define CloudWatch Events target to trigger Lambda function
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.lambda_trigger_rule.name
  arn  = aws_lambda_function.cost_notification_lambda.arn
}