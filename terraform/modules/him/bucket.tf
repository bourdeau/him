# Bucket for Django assets
resource "google_storage_bucket" "medias" {
  name          = "him-medias-${var.stage}"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket" "hyperion" {
  count         = var.is_prod ? 1 : 0
  name          = "him-gitlab-assets"
  location      = var.region
  force_destroy = true
}