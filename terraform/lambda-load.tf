data "archive_file" "lambda_load" {
    type        = "zip"
    source_dir  = "${path.module}/${var.lambda_load_source_dir}"
    excludes    = var.lambda_comp_exclude_list
    output_path = "${path.module}/../.remote_deployment/lambda_load.zip"
}

resource "aws_lambda_function" "lambda_load" {
    filename          = data.archive_file.lambda_load.output_path
    function_name     = "lambda_load"
    role             = aws_iam_role.load_lambda_role.arn
    handler          = "load.lambda_handler"
    timeout          = 180
    source_code_hash = data.archive_file.lambda_load.output_base64sha256
    runtime          = "python3.12"
    layers          = [aws_lambda_layer_version.layer_requests.arn,
                       "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14"]
    depends_on       = [aws_cloudwatch_log_group.load_log_group]
    
    environment {
      variables = {
            processing_bucket = aws_s3_bucket.s3_processing.bucket
            database         = aws_db_instance.weather_db.endpoint
            code_bucket      = aws_s3_bucket.s3_code.bucket
            DB_HOST     = aws_db_instance.weather_db.endpoint
            DB_PORT     = aws_db_instance.weather_db.port
            DB_NAME     = aws_db_instance.weather_db.db_name
            DB_USER     = var.database_user
            DB_PASSWORD = var.database_password
      }
    } 

    vpc_config {
      subnet_ids         = [aws_db_instance.weather_db.subnet_group_name]
      security_group_ids = [aws_security_group.lambda_sg.id]
    }
}

# Create security group for Lambda
resource "aws_security_group" "lambda_sg" {
  name        = "lambda-load-sg"
  description = "Security group for Load Lambda"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}