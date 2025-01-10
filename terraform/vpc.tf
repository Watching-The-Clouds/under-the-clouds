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