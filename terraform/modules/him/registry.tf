resource "google_artifact_registry_repository" "him" {
    count         = var.is_prod ? 1 : 0
    location      = var.region
    repository_id = "him"
    description   = "him Registery"
    format        = "DOCKER"
}