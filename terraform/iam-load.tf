# Create load lambda role
resource "aws_iam_role" "load_lambda_role" {
  name_prefix        = "role-load-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_policy.json
}

#Create load lambda policy
resource "aws_iam_policy" "load_lambda_policy" {
  name        = "load-lambda-policy"
  description = "IAM policy for Lambda to access S3 buckets, CloudWatch logs, and RDS"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:GetObject"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-code/*"
      },

      {
        Action = ["s3:ListBucket"],
        Effect = "Allow",
        Resource = "arn:aws:s3:::${var.project_name}-processing"
      },
      {
        Action = ["s3:GetObject"],
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
        Resource = "arn:aws:logs:eu-west-2:619071356744:log-group:/aws/lambda/lambda_load:*"
      },
      {
        Action = ["sns:Publish"],
        Effect = "Allow",
        Resource = "arn:aws:sns:eu-west-2:619071356744:alert-sre"
      },
      {
        Effect = "Allow",
        Action = [
          "rds-db:connect",
          "rds:DescribeDBInstances",
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement"
        ],
        Resource = aws_db_instance.weather_db.arn
      },
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
          "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses"
        ],
        Resource = "*"
      }
    ]
  })
}

#Attach policy to the role
resource "aws_iam_role_policy_attachment" "load_lambda_policy_attach" {
  role       = aws_iam_role.load_lambda_role.name
  policy_arn = aws_iam_policy.load_lambda_policy.arn
}
