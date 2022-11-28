# Bucket for Django assets
resource "google_storage_bucket" "medias" {
  name          = "him-medias-${var.stage}"
  location      = var.region
  force_destroy = true
}