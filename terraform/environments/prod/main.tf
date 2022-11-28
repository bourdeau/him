terraform {
  required_version = ">= 1.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.43"
    }
    random = ">= 3.4.3"
  }
  cloud {
    organization = "him"

    workspaces {
      name = "him-prod"
    }
  }
}


module "him" {
  source  = "../../modules/him"

  stage = "prod"
  is_prod = true
  db_settings = {
    tier              = "db-custom-2-4096"
    availability_type = "ZONAL"
    retained_backups  = 3
  }
  cr_api_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "1"
    max_scale      = "10"
  }
  cr_worker_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "1"
    max_scale      = "10"
  }
  cr_bookreco_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "1"
    max_scale      = "10"
  }
}