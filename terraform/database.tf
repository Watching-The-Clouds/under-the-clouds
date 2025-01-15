resource "aws_db_instance" "weather_db" {
  identifier           = "weather-forecasts"
  engine              = "postgres"
  engine_version      = "15.10"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_encrypted   = true

  db_name             = "weather_forecasts"
  username           = var.database_user
  password           = var.database_password

  skip_final_snapshot = true  # For development; set to false in production
  
  # Free tier settings
  publicly_accessible = false
  multi_az           = false

  # Enable automated backups
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  
  # Performance insights (free for t3.micro)
  performance_insights_enabled = true
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name = "weather-forecasts-db"
    Project = var.project_name
  }
}

# Output the database endpoint
output "db_endpoint" {
  value = aws_db_instance.weather_db.endpoint
}

# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "weather-db-security-group"
  description = "Security group for weather forecast database"

  # Allow access from VPC CIDR
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["172.31.0.0/16"]  # Your VPC CIDR
  }

  # Allow access from Lambda security group
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "weather-db-sg"
  }
}
