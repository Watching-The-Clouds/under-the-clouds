resource "aws_lambda_function" "lambda_load" {
    function_name       = "lambda_load"
    s3_bucket           = aws_s3_bucket.s3_code.bucket
    s3_key              = "lambda_load.zip"
    role                = aws_iam_role.load_lambda_role.arn
    handler             = "load.lambda_handler"
    timeout             = 180
    source_code_hash    = data.archive_file.lambda_transform.output_base64sha256
    runtime             = "python3.12"
  layers           = [
    "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14" 
  ]
    depends_on          = [aws_cloudwatch_log_group.load_log_group]
    environment {
      variables = {
            processing_bucket = aws_s3_bucket.s3_processing.bucket
            database = aws_db_instance.weather_db.endpoint
            code_bucket         = aws_s3_bucket.s3_code.bucket
      }
    } 
}

data "archive_file" "lambda_load" {
    type        = "zip"
    source_dir  = "${path.module}/${var.lambda_load_source_dir}"
    excludes    = var.lambda_comp_exclude_list
    output_path = "${path.module}/../.remote_deployment/lambda_load.zip"
}