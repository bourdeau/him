# Lessons learned the hard way

### Never use `*_iam_policy`! NEVER!
It is authoritative! It will destroy Google default services accounts which are created when you activate a [Google Cloud API](https://console.cloud.google.com/apis/dashboard?project=him).
Once these accounts are destroyed, you can't create them back. They will be automatically destroyed by a Google worker.
Even if you disable the API and enable it again. The only solution is to destroy the projet and create a new one.

### Region
Region is important. Some services are enabled in some region and some are not. For instance the [Google Cloud Scheduler](https://cloud.google.com/scheduler) is not available in `euwest9`. That's why I switched to `euwest3`. Don't change the region please.

### Never CRUD ressouces throug the Google Cloud Console
Just code what you need in HCL. Otherwise you will have strange behaviours. Adding stuff manually is like in the old days when people usse to ssh admin@prodserver and use to edit some code with vim. Then you wonder why everything is fucked up.

### Don't add Google API ressources
Do not add the Google APIs in the HCL ressources. Theses API are needed by Terraform to CRUD ressources. If you add them in your code you will have troubles. Just activate them once by doing:
```bash
gcloud config set project him

gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  cloudresourcemanager.googleapis.com \
  compute.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com \
  cloudscheduler.googleapis.com \
  sqladmin.googleapis.com
```

### Projets and stages
Google Projects are not designed to be used as stages. It seems obvious because the word Project != Stage but I made the mistake. Because then you will need to have a lot of cross dependencies between projects and you often apply some changes to the wrong place.

### Apply, Destroy, Apply
If you can't make `terraform destroy` and `terraform apply` without having to do something manually in between, it means you are doing it wrong.


### Do not create ressource for Service account keys
Otherwise they will be in the Terraform state. If someone hack your Terraform Cloud account and get the state, it will egt the keys.