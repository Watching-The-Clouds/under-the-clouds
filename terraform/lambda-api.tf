data "archive_file" "lambda_api" {
    type        = "zip"
    source_dir  = "${path.module}/${var.lambda_api_source_dir}"
    excludes    = var.lambda_comp_exclude_list
    output_path = "${path.module}/../.remote_deployment/lambda_api.zip"
}

resource "aws_lambda_function" "lambda_api" {
    function_name       = "lambda_api"
    s3_bucket           = aws_s3_bucket.s3_code.bucket
    s3_key              = "lambda_api.zip"
    role                = aws_iam_role.api_role.arn
    handler             = "app.handler"
    timeout             = 180
    source_code_hash    = data.archive_file.lambda_api.output_base64sha256
    runtime             = "python3.12"
    layers              = [aws_lambda_layer_version.layer_requests.arn]
    depends_on = [
        data.archive_file.lambda_api,
        aws_lambda_layer_version.layer_requests
    ]
    environment {
      variables = {
            CODE_BUCKET         = aws_s3_bucket.s3_code.bucket
            DB_HOST     = split(":", aws_db_instance.weather_db.endpoint)[0]
            DB_PORT     = tostring(aws_db_instance.weather_db.port)
            DB_NAME     = aws_db_instance.weather_db.db_name
            DB_USER     = var.database_user
            DB_PASSWORD = var.database_password
      }
    } 
    vpc_config {
      subnet_ids         = data.aws_subnets.default.ids
      security_group_ids = [aws_security_group.lambda_api_sg.id]
    }
}

resource "aws_security_group" "lambda_api_sg" {
  name        = "lambda-api-security-group"
  description = "Security group for API Lambda function"
  vpc_id      = data.aws_vpc.default.id

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "lambda-api-sg"
  }
}