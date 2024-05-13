resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "BUCKETNAME"
}

resource "aws_s3_object" "lambda_object" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "lambda_function.zip"
  source = var.python_script
}