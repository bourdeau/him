# Create Cloud Run Django API service
resource "google_cloud_run_service" "him_api" {
  name                       = "him-api-${var.stage}"
  location                   = var.region
  autogenerate_revision_name = true

  template {
    spec {
      service_account_name = google_service_account.him_api.email
      containers {
        image = "europe-west3-docker.pkg.dev/him/him/him-api"
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

# Create Cloud Run Worker service
resource "google_cloud_run_service" "him_worker" {
  name                       = "gleeephpro-worker-${var.stage}"
  location                   = var.region
  autogenerate_revision_name = true

  template {
    spec {
      service_account_name = google_service_account.him_worker.email
      containers {
        image = "europe-west3-docker.pkg.dev/him/him/him-worker"
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
            cpu    = var.cr_worker_settings.cpu
            memory = var.cr_worker_settings.memory
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = var.cr_worker_settings.min_scale
        "autoscaling.knative.dev/maxScale"      = var.cr_worker_settings.max_scale
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.instance.connection_name
        "run.googleapis.com/client-name"        = "terraform"
        "run.googleapis.com/cpu-throttling"     = var.cr_worker_settings.cpu_throttling
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

# Create Cloud Run Bookreco service
resource "google_cloud_run_service" "bookreco" {
  name                       = "bookreco-${var.stage}"
  location                   = var.region
  autogenerate_revision_name = true

  template {
    spec {
      service_account_name = google_service_account.bookreco.email
      containers {
        image = "europe-west3-docker.pkg.dev/him/him/bookrecoapi"
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
            cpu    = var.cr_worker_settings.cpu
            memory = var.cr_worker_settings.memory
          }
        }
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = var.cr_worker_settings.min_scale
        "autoscaling.knative.dev/maxScale"      = var.cr_worker_settings.max_scale
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.instance.connection_name
        "run.googleapis.com/client-name"        = "terraform"
        "run.googleapis.com/cpu-throttling"     = var.cr_worker_settings.cpu_throttling
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