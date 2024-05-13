resource "aws_iam_role" "lambda_role" {
  name = "lambda_cost_notification_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  inline_policy {
    name = "lambda_cost_notification_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect   = "Allow"
          Action   = "ce:GetCostAndUsage"
          Resource = "*"
        }
      ]
    })
  }
}