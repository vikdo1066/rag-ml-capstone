variable "project_id" {
  type        = string
  description = "The GCP Project ID"
  default     = "dt-vdogic-sandbox-dev"
}

variable "region" {
  type        = string
  description = "GCP Region for resources"
  default     = "europe-west8"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository in format 'owner/repo'"
  default     = "vikdo1066/rag-ml-capstone"
}

variable "support_email" {
  type        = string
  description = "Support email for the IAP Brand (must be your email or a Workspace group)"
  default     = "viktor.dogic@datatonic.com"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)"
  default     = "dev"
}

variable "engagement" {
  type        = string
  description = "Short engagement code"
  default     = "sandbox"
}

variable "team" {
  type        = string
  description = "Owning team name"
  default     = "platform"
}

variable "cost_center" {
  type        = string
  description = "Engagement billing code"
  default     = "cc-1234"
}

variable "billing_account_id" {
  type        = string
  description = "GCP Billing Account ID (Required for budget alerts)"
  default     = "" # Optional: populate if configuring google_billing_budget
}

variable "alert_email_address" {
  type        = string
  description = "Shared team email / distribution list for budget alerts"
  default     = "team-alerts@example.com"
}