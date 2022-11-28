# Artifact Registry Readers
resource "google_project_iam_member" "artifactregistry_reader" {
  count   = var.is_prod ? 1 : 0
  project = var.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-716987057949@serverless-robot-prod.iam.gserviceaccount.com"
}

# Run Admin
resource "google_project_iam_member" "run_admin" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:716987057949@cloudbuild.gserviceaccount.com",
  ])

  role = "roles/run.admin"
  member = "${each.key}"
}

# Service Account Users
resource "google_project_iam_member" "iam_serviceAccountUser" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:716987057949@cloudbuild.gserviceaccount.com",
  ])

  role = "roles/iam.serviceAccountUser"
  member = "${each.key}"
}

# Cloud SQL Clients
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:716987057949@cloudbuild.gserviceaccount.com",
  ])

  role = "roles/cloudsql.client"
  member = "${each.key}"
}

# Storage object viewers
resource "google_project_iam_member" "storage_objectViewer" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
  ])

  role = "roles/storage.objectViewer"
  member = "${each.key}"
}

# Secret Manager Secret Accessors
resource "google_project_iam_member" "secretmanager_secretAccessor" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:716987057949@cloudbuild.gserviceaccount.com"
  ])

  role = "roles/secretmanager.secretAccessor"
  member = "${each.key}"
}