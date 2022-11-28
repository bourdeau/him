# Scheduler for the Worker
resource "google_cloud_scheduler_job" "worker_job" {
  name             = "worker-job-${var.stage}"
  description      = "Scheduler for the worker"
  schedule         = "0 */3 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "1800s"

  http_target {
    http_method = "GET"
    uri         = google_cloud_run_service.him_worker.status[0].url

    oidc_token {
      service_account_email = data.google_compute_default_service_account.default.email
    }
  }
}
