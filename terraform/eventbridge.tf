resource "aws_cloudwatch_event_rule" "scheduler" {
  name                = "every-three-hours"
  description         = "runs-every-3-hours"
  schedule_expression = "rate(180 minutes)"
  state              = "ENABLED"
}

resource "aws_cloudwatch_event_target" "lambda-target-3-hours" {
    rule = aws_cloudwatch_event_rule.scheduler.name
    target_id = "run-extraction"
    arn = aws_lambda_function.lambda_extract.arn
}

resource "aws_lambda_permission" "allow_eventbridge_to_call_extract" {
    statement_id = "AllowExecutionFromCloudWatchExtract"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_extract.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.scheduler.arn
}
