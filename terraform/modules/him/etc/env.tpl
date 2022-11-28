# Django Settings
POSTGRES_HOST=/cloudsql/${instance.project}:${instance.region}:${instance.name}
POSTGRES_DB=${database.name}
POSTGRES_USER=${user.name}
POSTGRES_PASSWORD=${user.password}
GS_BUCKET_NAME="${bucket}"
SECRET_KEY="${secret_key}"