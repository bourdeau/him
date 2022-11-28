# Default Google Compute Service (@cloudbuild.gserviceaccount.com)
# Used by the Scheduler
data "google_compute_default_service_account" "default" {
}

# Service Account for the Django API
resource "google_service_account" "him_api" {
  account_id   = "him-api-${var.stage}"
  display_name = "Django (${var.stage})"
  description  = "Service account for him Django API"
}

locals {
  him_api_sa = "serviceAccount:${google_service_account.him_api.email}"
}