resource "aws_iam_role" "extract_role" {
    name                = "extract_role"
    assume_role_policy  = data.aws_iam_policy_document.lambda_policy.json 
}

resource "aws_iam_policy" "extract_lambda_policy" {
  name        = "extract-lambda-policy"
  description = "IAM policy for Lambda to access S3 buckets and CloudWatch logs"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject", "s3:PutObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-code/*"
      },
      {
        Action = ["s3:PutObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-ingestion/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        
        Effect = "Allow",
        Resource = "arn:aws:logs:eu-west-2:418295700587:log-group:/aws/lambda/lambda_extract:*"
      },
      # {
      #   Action = ["secretsmanager:GetSecretValue"],
      #   Effect = "Allow",
      #   Resource = "arn:aws:secretsmanager:eu-west-2:${data.aws_caller_identity.current.account_id}:secret:api_key*"
      # },
      {
        Action = ["sns:Publish"],
        Effect = "Allow",
        Resource = "arn:aws:sns:eu-west-2:418295700587:extract-errors-topic"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "extract_cloudwatch_policy_attachment" {
    role        = aws_iam_role.extract_role.name
    policy_arn  = aws_iam_policy.extract_cloudwatch_policy.arn
}

### TODO: SNS Policies