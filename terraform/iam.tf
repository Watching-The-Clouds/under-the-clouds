data "aws_iam_policy_document" "lambda_policy" {
    statement {
        effect  = "Allow"
        actions = ["sts:AssumeRole"]
        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"] 
        } 
    }
}

data "aws_iam_policy_document" "cloudwatch_policy" {
    statement {
        effect      = "Allow"
        actions     = [ "logs:CreateLogStream",
                        "logs:PutLogEvents"]
        resources   = ["arn:aws:logs:*:*:*"] 
    }
}

### TODO: IAM policy for Secrets Manager to access Endpoint DB

