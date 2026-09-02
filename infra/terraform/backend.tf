terraform {
  backend "gcs" {
    bucket = "dt-vdogic-sandbox-dev-tfstate"
    prefix = "terraform/state"
  }
}