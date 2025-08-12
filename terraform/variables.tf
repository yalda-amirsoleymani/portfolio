variable "aws_region" {
  default     = "eu-west-1"
  description = "AWS Region"
}
variable "db_username" {
  description = "DB username"
  type        = string
}

variable "db_password" {
  description = "DB password"
  type        = string
  sensitive   = true
}

