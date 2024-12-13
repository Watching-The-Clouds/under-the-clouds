resource "aws_sns_topic" "alert_sre" {
  name = "alert-sre"
}

resource "aws_sns_topic_subscription" "sre_email_subscription" {
  topic_arn = aws_sns_topic.alert_sre.arn
  protocol  = "email"
  endpoint  = "irina.redactor@gmail.com"
}