# SECRETS
resource "random_password" "django_secret_key" {
  special = false
  length  = 50
}

resource "google_secret_manager_secret" "django_settings" {
  secret_id = "django_settings-${var.stage}"

  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "django_settings" {
  secret = google_secret_manager_secret.django_settings.id

  secret_data = templatefile("${path.module}/etc/env.tpl", {
    bucket     = google_storage_bucket.medias.name
    secret_key = random_password.django_secret_key.result
    user       = google_sql_user.him
    instance   = google_sql_database_instance.instance
    database   = google_sql_database.database
  })
}