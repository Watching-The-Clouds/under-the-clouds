resource "aws_s3_bucket" "s3_code" {
    bucket      = "${var.project_name}-code"
    tags        = {
        name = "Code Bucket"
        environment = "dev"
        description = "S3 bucket to store and provide lambda_handler code for lambdas."
    }
}

resource "aws_s3_bucket" "s3_ingestion" {
    bucket      = "${var.project_name}-ingestion"
    tags        = {
        name = "Ingestion Bucket"
        environment = "dev"
        description = "S3 bucket to store extracted JSON from OpenWeather API queries."
    }
}

resource "aws_s3_bucket" "s3_processing" {
    bucket      = "${var.project_name}-processing"
    tags        = {
        name = "Processing Bucket"
        environment = "dev"
        description = "S3 Bucket to store processed data from Transformation Lambda"
    }
}

resource "aws_s3_object" "lambda-extract" {
    bucket      = aws_s3_bucket.s3_code.bucket
    key         = "lambda_extract.zip"
    source      = data.archive_file.lambda_extract.output_path
    etag        = filemd5(data.archive_file.lambda_extract.output_path)
    depends_on  = [ aws_s3_object.layer_requests ]
}

resource "aws_s3_object" "layer_requests" {
    bucket      = aws_s3_bucket.s3_code.bucket
    key         = "layer_requests.zip"
    source      = "${path.module}/${var.layer_requests_file}"
    etag        = filemd5("${path.module}/${var.layer_requests_file}")
    depends_on  = [ var.layer_requests_file ]
}

# resource "aws_s3_bucket_notification" "ingestion_bucket_notification" {
#   bucket = aws_s3_bucket.ingested_data_bucket.id

#   lambda_function {
#     lambda_function_arn = aws_lambda_function.transform.arn
#     events              = ["s3:ObjectCreated:*"]
#   }
# }

# resource "aws_lambda_permission" "s3_trigger" {
#   statement_id  = "AllowS3Invoke"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.transform.function_name
#   principal     = "s3.amazonaws.com"
#   source_arn    = "aws_s3_bucket.${var.project_name}-ingestion.arn"
# }
