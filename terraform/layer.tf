resource "aws_lambda_layer_version" "layer_requests" {
    layer_name      = "layer_requests"
    description     = "Installs Python Requests library"
    s3_bucket       = aws_s3_object.layer_requests.bucket
    s3_key          = aws_s3_object.layer_requests.key
}