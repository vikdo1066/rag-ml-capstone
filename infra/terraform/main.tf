terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ------------------------------------------------------------------------------
# 1. Project Services (APIs)
# ------------------------------------------------------------------------------
locals {
  services = [
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iap.googleapis.com",
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "storage.googleapis.com",
    "secretmanager.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ]
  common_labels = {
    engagement  = var.engagement
    environment = var.environment
    team        = var.team
    cost_center = var.cost_center
    managed_by  = "terraform"
  }
}

resource "google_project_service" "required_apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = false
}

# ------------------------------------------------------------------------------
# 2. Artifact Registry Repository
# ------------------------------------------------------------------------------
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "app-repo"
  description   = "Docker repository for service deployments"
  format        = "DOCKER"

  depends_on = [google_project_service.required_apis]

  labels = merge(local.common_labels, {
    feature = "containers"
  })
}

# ------------------------------------------------------------------------------
# 3. Workload Identity Federation (WIF) for GitHub Actions
# ------------------------------------------------------------------------------
resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-pool"
  display_name              = "GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions CI/CD"

  depends_on = [google_project_service.required_apis]
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                        = "GitHub Provider"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  # Attribute mapping condition pinning to your specific repository
  attribute_condition = "assertion.repository == '${var.github_repo}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# ------------------------------------------------------------------------------
# 4. Deploy Service Account & Roles
# ------------------------------------------------------------------------------
resource "google_service_account" "deploy_sa" {
  account_id   = "github-deployer"
  display_name = "CI/CD Deployment Service Account"
}

# Grant required roles to the deployment Service Account
locals {
  deploy_sa_roles = [
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.writer"
  ]
}

resource "google_project_iam_member" "deploy_sa_bindings" {
  for_each = toset(local.deploy_sa_roles)
  project  = var.project_id
  role     = each.key
  member   = "serviceAccount:${google_service_account.deploy_sa.email}"
}

# Allow GitHub Actions (via WIF) to impersonate the deploy Service Account
resource "google_service_account_iam_member" "wif_sa_impersonation" {
  service_account_id = google_service_account.deploy_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/${var.github_repo}"
}

# ------------------------------------------------------------------------------
# 5. IAP Brand (OAuth Consent Screen)
# ------------------------------------------------------------------------------
resource "google_iap_brand" "iap_brand" {
  support_email     = var.support_email
  application_title = "Internal IAP Application"
  project           = var.project_id

  depends_on = [google_project_service.required_apis]
}