# Owners
resource "google_project_iam_member" "owner_ph" {
  count   = var.is_prod ? 1 : 0
  project = var.project
  role    = "roles/owner"
  member  = "user:ph@gleeph.net"
}

# Artifact Registry Readers
resource "google_project_iam_member" "artifactregistry_reader" {
  count   = var.is_prod ? 1 : 0
  project = var.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-557015977363@serverless-robot-prod.iam.gserviceaccount.com"
}

# Run Admin
resource "google_project_iam_member" "run_admin" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:557015977363@cloudbuild.gserviceaccount.com",
  ])

  role = "roles/run.admin"
  member = "${each.key}"
}

# Service Account Users
resource "google_project_iam_member" "iam_serviceAccountUser" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:557015977363@cloudbuild.gserviceaccount.com",
  ])

  role = "roles/iam.serviceAccountUser"
  member = "${each.key}"
}

# Cloud SQL Clients
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project
  for_each = toset([
    local.him_api_sa,
    "serviceAccount:557015977363@cloudbuild.gserviceaccount.com",
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
    "serviceAccount:557015977363@cloudbuild.gserviceaccount.com"
  ])

  role = "roles/secretmanager.secretAccessor"
  member = "${each.key}"
}


# Bucket objects are pubicly accessible
resource "google_storage_default_object_access_control" "public_rule" {
  count  = var.is_prod ? 1 : 0
  bucket = google_storage_bucket.hyperion[0].name
  role   = "READER"
  entity = "allUsers"
}


# Specify Cloud Run permissions
# All users can access the service
# data "google_iam_policy" "noauth" {
#   binding {
#     role = "roles/run.invoker"
#     members = [
#       "allUsers",
#     ]
#   }
# }


# No Auth needed to access the Django API (remove later)
# resource "google_cloud_run_service_iam_binding" "noauth" {
#   location = google_cloud_run_service.him_api.location
#   project  = google_cloud_run_service.him_api.project
#   service  = google_cloud_run_service.him_api.name

#   policy_data = data.google_iam_policy.noauth.policy_data
# }