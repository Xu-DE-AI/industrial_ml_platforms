terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  default = "eu-central-1"
}

variable "data_bucket" {
  type = string
}

resource "aws_s3_bucket" "lake" {
  bucket = var.data_bucket
}

resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "lake_bucket" {
  value = aws_s3_bucket.lake.bucket
}

# Production extensions:
# IAM role / workload identity
# KMS
# ECR
# EKS
# VPC
# CloudWatch
# private endpoints
