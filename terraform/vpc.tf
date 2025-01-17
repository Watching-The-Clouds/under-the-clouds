resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.default.id
  service_name = "com.amazonaws.eu-west-2.s3"
  vpc_endpoint_type = "Gateway"
}

# Associate with route table
resource "aws_vpc_endpoint_route_table_association" "s3_endpoint" {
  route_table_id  = data.aws_route_table.default.id
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}

# Get default route table
data "aws_route_table" "default" {
  vpc_id = data.aws_vpc.default.id
  filter {
    name   = "association.main"
    values = ["true"]
  }
}

# Add these VPC endpoints for Lambda to access AWS services
resource "aws_vpc_endpoint" "logs" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.eu-west-2.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids        = data.aws_subnets.default.ids
  security_group_ids = [aws_security_group.lambda_api_sg.id]

  private_dns_enabled = true
}

resource "aws_vpc_endpoint" "sns" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.eu-west-2.sns"
  vpc_endpoint_type = "Interface"
  subnet_ids        = data.aws_subnets.default.ids
  security_group_ids = [aws_security_group.lambda_api_sg.id]

  private_dns_enabled = true
}

# If you're using API Gateway, you'll also need this
resource "aws_vpc_endpoint" "execute_api" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.eu-west-2.execute-api"
  vpc_endpoint_type = "Interface"
  subnet_ids        = data.aws_subnets.default.ids
  security_group_ids = [aws_security_group.lambda_api_sg.id]

  private_dns_enabled = true
} 