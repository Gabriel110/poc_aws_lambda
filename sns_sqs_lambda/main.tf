provider "aws" {
  region                      = var.region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    lambda     = "http://localhost:4566"
    cloudwatch = "http://localhost:4566"
    iam        = "http://localhost:4566"
    sns        = "http://localhost:4566"
    sqs        = "http://localhost:4566"
  }
}

resource "aws_lambda_function" "lambda_function" {
  function_name    = "lambda-process"
  filename         = data.archive_file.lambda_zip_file.output_path
  source_code_hash = data.archive_file.lambda_zip_file.output_base64sha256
  handler          = "handler.handler"
  role             = aws_iam_role.lambda_assume_role.arn
  runtime          = "python3.8"
  layers           = [aws_lambda_layer_version.lambda_function_layer.arn]

  lifecycle {
    create_before_destroy = true
  }
}

data "archive_file" "lambda_zip_file" {
  output_path = "${path.module}/lambda_zip/lambda.zip"
  source_dir  = "${path.module}/lambda"
  excludes    = ["__init__.py", "*.pyc"]
  type        = "zip"
}

resource "null_resource" "build_lambda_layers" {
  provisioner "local-exec" {
    command = "${path.module}/build.sh"
  }
}

resource "aws_lambda_layer_version" "lambda_function_layer" {
  filename            = data.archive_file.lambda_zip_file.output_path
  source_code_hash    = data.archive_file.lambda_zip_file.output_base64sha256
  layer_name          = "lambda-function-layer"
  compatible_runtimes = ["python3.8", "python3.6", "python3.7"]
}

resource "aws_sns_topic" "sns_topic" {
  name = "sns-lambda"
}

resource "aws_sns_topic" "sns_topic_dois" {
  name = "sns-lambda-dois"
}

resource "aws_sqs_queue" "queue" {
  name                      = "sqs-lambda"
  receive_wait_time_seconds = 20
  message_retention_seconds = 18400
}

resource "aws_sqs_queue" "queue_dois" {
  name                      = "sqs-lambda-dois"
  receive_wait_time_seconds = 20
  message_retention_seconds = 18400
}

resource "aws_sns_topic_subscription" "queue_subscription" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.sns_topic.arn
  endpoint             = aws_sqs_queue.queue.arn
}

resource "aws_sns_topic_subscription" "queue_subscription_dois" {
  protocol             = "sqs"
  raw_message_delivery = true
  topic_arn            = aws_sns_topic.sns_topic_dois.arn
  endpoint             = aws_sqs_queue.queue_dois.arn
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn  = aws_sqs_queue.queue.arn
  function_name     = aws_lambda_function.lambda_function.arn
  enabled           = true
  batch_size        = 1
  starting_position = "LATEST"
}