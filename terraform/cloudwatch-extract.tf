resource "aws_cloudwatch_log_group" "extract_log_group" {
    name                = "/aws/lambda/${aws_lambda_function.lambda_extract.function_name}"
    retention_in_days   = 30 # ADJUST AS NECESSARY
    tags                =  {
        name        = "Extract Lambda log group"
        environment = "dev"
        description = "Extract Lambda log group"
    }
}

resource "aws_cloudwatch_log_metric_filter" "log_errors_for_extract_lambda" {
    name            = "extract_error"
    pattern         = "ERROR"
    log_group_name  = aws_cloudwatch_log_group.extract_log_group.name
    metric_transformation {
      name          = "extract_error"
      namespace     = "log_errors"
      value         = 1
    }
}

resource "aws_cloudwatch_metric_alarm" "error_count_alarm_for_extract_lambda" {
    alarm_name                  = "extract_error"
    comparison_operator         = "GreaterThanOrEqualToThreshold"
    evaluation_periods          = 1
    metric_name                 = aws_cloudwatch_log_metric_filter.log_errors_for_extract_lambda.name
    namespace                   = "log_errors"
    period                      = 600 # ADJUST AS NECESSARY
    statistic                   = "SampleCount"
    threshold                   = 1
    alarm_description           = "Error logged in Extract Lambda"
    treat_missing_data          = "notBreaching"
    insufficient_data_actions   = []
}