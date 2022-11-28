output "service_url" {
  value       = google_cloud_run_service.him_api.status[0].url
  description = "URL of the Django API"
}