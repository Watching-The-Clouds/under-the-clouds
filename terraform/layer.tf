resource "aws_lambda_layer_version" "requests_layer" {
    layer_name      = "requests_layer"
    s3_bucket       = aws_s3_object.layer_requests.bucket
    s3_key          = aws_s3_object.layer_requests.key
}