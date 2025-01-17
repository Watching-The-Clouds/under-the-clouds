resource "aws_iam_role" "api_role" {
    name                = "api_role"
    assume_role_policy  = data.aws_iam_policy_document.lambda_policy.json 
}

resource "aws_iam_policy" "api_lambda_policy" {
    name = "api-lambda-policy"
    description = "IAM policy for API Lambda to access S3,RDS,ENI and CloudWatch logs"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = ["s3:GetObject"],
                Effect = "Allow",
                Resource = "arn:aws:s3:::${var.project_name}-code/*"
            },
            {
                Action = [
                    "rds-db:connect",
                    "rds:DescribeDBInstances"
                ],
                Effect = "Allow",
                Resource = "*"
            },
            {
                Action = [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                Effect = "Allow",
                Resource = [
                    "${aws_cloudwatch_log_group.api_log_group.arn}",
                    "${aws_cloudwatch_log_group.api_log_group.arn}:*"
                ]
            },
            {
                Action = [
                    "sns:Publish"
                ],
                Effect = "Allow",
                Resource = "arn:aws:sns:eu-west-2:619071356744:api-errors-topic"
            },
            {
                Action = [
                    "ec2:CreateNetworkInterface",
                    "ec2:DescribeNetworkInterfaces",
                    "ec2:DeleteNetworkInterface"
                ],
                Effect = "Allow",
                Resource = "*"
            },
            {
                Action = [
                    "execute-api:Invoke",
                    "execute-api:ManageConnections"
                ],
                Effect = "Allow",
                Resource = "arn:aws:execute-api:*:*:*"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "api_lambda_policy_attachment" {
    role        = aws_iam_role.api_role.name
    policy_arn  = aws_iam_policy.api_lambda_policy.arn
}