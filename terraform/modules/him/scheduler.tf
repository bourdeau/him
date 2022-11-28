# Scheduler for the Bot
resource "google_cloud_scheduler_job" "bot_job" {
  name             = "bot-job-${var.stage}"
  description      = "Scheduler for the bot"
  schedule         = "0 */3 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "1800s"

  http_target {
    http_method = "GET"
    uri         = google_cloud_run_service.him_api.status.url

    oidc_token {
      service_account_email = data.google_compute_default_service_account.default.email
    }
  }
}
