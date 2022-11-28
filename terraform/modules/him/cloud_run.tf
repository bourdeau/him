# Create Cloud Run Django API service
resource "google_cloud_run_service" "him_api" {
  name                       = "him-api-${var.stage}"
  location                   = var.region
  autogenerate_revision_name = true

  template {
    spec {
      service_account_name = google_service_account.him_api.email
      containers {
        image = "europe-west3-docker.pkg.dev/him/him-api"
        env {
          name  = "CLOUD_RUN_ENV"
          value = var.stage
        }
        env {
          name  = "SETTINGS_NAME"
          value = "django_settings-${var.stage}"
        }
        resources {
          limits = {
            cpu    = var.cr_api_settings.cpu
            memory = var.cr_api_settings.memory
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = var.cr_api_settings.min_scale
        "autoscaling.knative.dev/maxScale"      = var.cr_api_settings.max_scale
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.instance.connection_name
        "run.googleapis.com/client-name"        = "terraform"
        "run.googleapis.com/cpu-throttling"     = var.cr_api_settings.cpu_throttling

      }
      labels = {
        env : var.stage
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}