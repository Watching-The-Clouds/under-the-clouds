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