resource "aws_lambda_function" "lambda_extract" {
    function_name       = "lambda_extract"
    s3_bucket           = aws_s3_bucket.s3_code.bucket
    s3_key              = "lambda_extract.zip"
    role                = aws_iam_role.extract_role.arn
    handler             = "extract.lambda_handler"
    timeout             = 180
    source_code_hash    = data.archive_file.lambda_extract.output_base64sha256
    runtime             = "python3.12"
    layers              = [aws_lambda_layer_version.layer_requests.arn]
    depends_on          = [aws_cloudwatch_log_group.extract_log_group]
    environment {
      variables = {
            api_key             = var.openweather_api_key
            ingestion_bucket    = aws_s3_bucket.s3_ingestion.bucket
            code_bucket         = aws_s3_bucket.s3_code.bucket
      }
    } 
}

data "archive_file" "lambda_extract" {
    type        = "zip"
    source_dir  = "${path.module}/${var.lambda_extract_source_dir}"
    excludes    = var.lambda_comp_exclude_list
    output_path = "${path.module}/../.remote_deployment/lambda_extract.zip"
}