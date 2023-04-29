module "api_gateway" {
  source        = "terraform-aws-modules/apigateway-v2/aws"

  name          = "visit-counter-api"
  description   = "API Gateway for visit counter"
  protocol_type = "HTTP"
  cors_configuration = {
    allow_origins = ["*"]
    allow_methods = ["GET", "OPTIONS"]
    allow_headers = ["content-type", 
                     "x-amz-date",
                     "authorization",
                     "x-api-key",
                     "x-amz-security-token"]
  }

  domain_name = " "
  domain_name_certificate_arn = ""

  default_stage_access_log_destination_arn = "arn:aws:logs:eu-west-1:835367859851:log-group:debug-apigateway"
  default_stage_access_log_format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"

  integrations = {
    "ANY /" = {
        lambda_arn = "arn:aws:lambda:${var.region}:${var.iam_access_id}:function:counter_function"
    }
  }
}