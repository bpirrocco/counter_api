variable "project_name" {
  default = "lambda-counter-terraform-github-actions"
}
variable "region" {
    default = "us-east-1"
}

variable "iam_access_id" {
    type        = string
    description = "My IAM Access ID"
}