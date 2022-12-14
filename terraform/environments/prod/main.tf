terraform {
  required_version = ">= 1.3"
  cloud {
    organization = "tinder-him"

    workspaces {
      name = "him-prod"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.43"
    }
    random = ">= 3.4.3"
  }
}


module "him" {
  source  = "../../modules/him"
  stage   = "prod"
  is_prod = true
  db_settings = {
    tier              = "db-custom-1-3840"
    availability_type = "ZONAL"
    retained_backups  = 1
  }
  cr_api_settings = {
    cpu            = "1000m"
    memory         = "2048Mi"
    cpu_throttling = false
    min_scale      = "0"
    max_scale      = "2"
  }
}