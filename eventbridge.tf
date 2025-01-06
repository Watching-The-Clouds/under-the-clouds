resource "aws_cloudwatch_event_rule" "scheduler" {
    name                = "every-three-hours"
    description         = "runs-every-3-hours"
    schedule_expression = "rate(180 minutes)"
    state              = "ENABLED"
} 