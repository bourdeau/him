# Schedulers for the Bot
resource "google_cloud_scheduler_job" "bot_like_profiles" {
  name             = "bot-like-profiles-${var.stage}"
  region           = var.region
  description      = "Scheduler for the bot"
  schedule         = "*/10 8-23 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "1800s"

  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_service.him_api.status[0].url}/bot/like/"

    # oidc_token {
    #   service_account_email = data.google_compute_default_service_account.default.email
    # }
  }
}
resource "google_cloud_scheduler_job" "bot_send_first_messages" {
  name             = "bot-send-first-messages-${var.stage}"
  region           = var.region
  description      = "Scheduler for the bot"
  schedule         = "*/20 10-22 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "1800s"

  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_service.him_api.status[0].url}/bot/send-first-messages/"

    # oidc_token {
    #   service_account_email = data.google_compute_default_service_account.default.email
    # }
  }
}
resource "google_cloud_scheduler_job" "bot_chat_with_matches" {
  name             = "bot-chat-with-matches-${var.stage}"
  region           = var.region
  description      = "Scheduler for the bot"
  schedule         = "*/2 10-23 * * *"
  time_zone        = "Europe/Paris"
  attempt_deadline = "1800s"

  http_target {
    http_method = "GET"
    uri         = "${google_cloud_run_service.him_api.status[0].url}/bot/chat-with-matches/"

    # oidc_token {
    #   service_account_email = data.google_compute_default_service_account.default.email
    # }
  }
}
