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
      name = "him-preprod"
    }
  }
}


module "him" {
  source  = "../../modules/him"

  stage = "preprod"
  is_prod = false
  db_settings = {
    tier              = "db-custom-2-4096"
    availability_type = "ZONAL"
    retained_backups  = 1
  }
  cr_api_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "0"
    max_scale      = "2"
  }
  cr_worker_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "0"
    max_scale      = "2"
  }
 cr_bookreco_settings = {
    cpu            = "2000m"
    memory         = "4096Mi"
    cpu_throttling = false
    min_scale      = "0"
    max_scale      = "2"
  }
}


