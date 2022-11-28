# POSTGRES DATABASE
resource "google_sql_database_instance" "instance" {
  name             = "him-${var.stage}"
  database_version = "POSTGRES_14"
  region           = var.region
  settings {
    tier              = var.db_settings.tier
    availability_type = var.db_settings.availability_type
    disk_autoresize   = true
    disk_type         = "PD_SSD"
    user_labels       = { "stage" = var.stage }
    insights_config {
      query_insights_enabled = true
    }
    backup_configuration {
      enabled    = true
      start_time = "00:00"
      backup_retention_settings {
        retained_backups = var.db_settings.retained_backups
        retention_unit   = "COUNT"
      }
    }
  }
  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "him"
  instance = google_sql_database_instance.instance.name
}


resource "google_sql_user" "him" {
  name     = "him"
  instance = google_sql_database_instance.instance.name
  password = random_password.database_password.result
}

resource "random_password" "database_password" {
  length  = 32
  special = false
}