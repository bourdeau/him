variable "project" {
  type        = string
  default     = "him"
  description = "The Project ID on GCP"
}

variable "stage" {
  type        = string
  description = "The stage (dev, preprod, prod)"
}

variable "is_prod" {
  type        = bool
  default     = false
  description = "Whether or not the env is prod"
}


variable "region" {
  type        = string
  default     = "europe-west3"
  description = "Google Cloud Region"
}

variable "db_settings" {
  type = object({
    tier              = string
    availability_type = string
    retained_backups  = number
  })
  description = "The Postgres database settings"
}

variable "cr_api_settings" {
  type = object({
    cpu            = string
    memory         = string
    cpu_throttling = bool
    min_scale      = string
    max_scale      = string
  })
  description = "The Cloud Run Django API settings"
}