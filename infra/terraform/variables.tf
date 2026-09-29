variable "project_id" {
  type        = string
  description = "The GCP Project ID"
}

variable "region" {
  type        = string
  description = "GCP Region for resources"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository in format 'owner/repo'"
}

variable "support_email" {
  type        = string
  description = "Support email for the IAP Brand (must be your email or a Workspace group)"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)"
}

variable "engagement" {
  type        = string
  description = "Short engagement code"
}

variable "team" {
  type        = string
  description = "Owning team name"
}

variable "cost_center" {
  type        = string
  description = "Engagement billing code"
}

variable "billing_account_id" {
  type        = string
  description = "GCP Billing Account ID (Required for budget alerts)"
}
