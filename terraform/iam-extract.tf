resource "aws_iam_role" "extract_role" {
    name                = "extract_role"
    assume_role_policy  = data.aws_iam_policy_document.assume_role_policy.json 
}

data "aws_iam_policy_document" "extract_s3_policy_document" {
    statement {
        effect      = "Allow"
        actions     = [ "S3:PutObject",
                        "S3:GetObject",
                        "S3:ListBucket"]
        resources   = [ "${aws_s3_bucket.s3_ingestion.arn}/*",
                        "${aws_s3_bucket.s3_ingestion.arn}"] 
    }
}

resource "aws_iam_policy" "extract_policy" {
    name    = "extract_s3_policy"
    policy  = data.aws_iam_policy_document.extract_s3_policy_document.json
}

resource "aws_iam_role_policy_attachment" "extract_s3_policy_attachment" {
    role        = aws_iam_role.extract_role.name
    policy_arn  = aws_iam_policy.extract_policy.arn 
}

resource "aws_iam_policy" "extract_cloudwatch_policy" {
    name    = "extract_cloudwatch_policy"
    policy  = data.aws_iam_policy_document.cloudwatch_policy.json
}

resource "aws_iam_role_policy_attachment" "extract_cloudwatch_policy_attachment" {
    role        = aws_iam_role.extract_role.name
    policy_arn  = aws_iam_policy.extract_cloudwatch_policy.arn
}

### TODO: SNS Policies