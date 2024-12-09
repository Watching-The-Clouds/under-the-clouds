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
    key         = "lambda-extract.zip"
    source      = data.archive_file.extract_lambda_handler.output_path
    etag        = filemd5(data.archive_file.extract_lambda_handler.output_path)
    depends_on  = [ data.archive_file.layer_requests  ]
}
