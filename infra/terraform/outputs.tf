output "artifact_repository" {
  value       = google_artifact_registry_repository.docker_repo.name
  description = "Artifact Registry repository name"
}

output "deploy_service_account_email" {
  value       = google_service_account.deploy_sa.email
  description = "Email of the deploy service account"
}

output "workload_identity_provider" {
  value       = google_iam_workload_identity_pool_provider.github_provider.name
  description = "Full provider name for GitHub Actions auth step"
}