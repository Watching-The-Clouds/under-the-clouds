# Create transform lambda role
resource "aws_iam_role" "transform_lambda_role" {
  name_prefix        = "role-transform-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_policy.json
}

#Create transformt lambda policy
resource "aws_iam_policy" "transform_lambda_policy" {
  name        = "transform-lambda-policy"
  description = "IAM policy for Lambda to access S3 buckets and CloudWatch logs"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-code/*"
      },
      {
        Action = ["s3:GetObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-ingestion/*"
      },
      {
        Action = ["s3:ListBucket"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-ingestion/*"
      },
      {
        Action = ["s3:ListBucket"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-processing"
      },
      {
        Action = ["s3:PutObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-processing/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect = "Allow",
        Resource = "arn:aws:logs:eu-west-2:418295700587:log-group:/aws/lambda/transform:*"
      },
      {
        Action = ["sns:Publish"],
        Effect = "Allow",
        Resource = "arn:aws:sns:eu-west-2:418295700587:alert-sre"
      }
    ]
  })
}

#Attach policy to the role
resource "aws_iam_role_policy_attachment" "transform_lambda_policy_attach" {
  role       = aws_iam_role.transform_lambda_role.name
  policy_arn = aws_iam_policy.transform_lambda_policy.arn
}
