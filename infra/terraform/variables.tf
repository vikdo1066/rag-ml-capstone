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
  default     = "YOUR_ORGANIZATION/YOUR_REPO_NAME" # <-- UPDATE THIS
}

variable "support_email" {
  type        = string
  description = "Support email for the IAP Brand (must be your email or a Workspace group)"
  default     = "your-email@example.com" # <-- UPDATE THIS
}