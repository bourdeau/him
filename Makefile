
DOCKER_BIN := `which docker`
DOCKER_COMPOSE_BIN := docker compose
PYTHON := python

# Colors
end = \033[0m
green = \033[92m
purple = \033[95m

default: help

.PHONY: help
help:
	@echo "$(purple)start$(end)                   start all containers as daemons"
	@echo "$(purple)dev-start$(end)               start all containers"
	@echo "$(purple)stop$(end)                    stop all containers"
	@echo "$(purple)shell-him$(end)         bash to him container"
	@echo "$(purple)migrate$(end)                 apply migrations"
	@echo "$(purple)makemigrations$(end)          create migrations"
	@echo "$(purple)collectstatic$(end)           generate Django statics files"
	@echo "$(purple)load-fixtures$(end)           load the fixtures in the Database"
	@echo "$(purple)pip-dev$(end)                 install dev requirements"
	@echo "$(purple)codestyle$(end)               apply codestyle"
	@echo "$(purple)test$(end)                    run tests"
	@echo "$(purple)cloud_sql_proxy_dev$(end)     start cloud_sql_proxy for dev"
	@echo "$(purple)cloud_sql_proxy_preprod$(end) start cloud_sql_proxy for preprod"
	@echo "$(purple)cloud_sql_proxy_prod$(end)    start cloud_sql_proxy for prod"
	@echo "$(purple)build$(end)                   build the docker image"
	@echo "$(purple)create-user-dev$(end)         create a user in dev environment"
	@echo "$(purple)create-user-preprod$(end)     create a user in preprod environment"
	@echo "$(purple)create-user-prod$(end)        create a user in prod environment"
	@echo "$(purple)deploy-dev$(end)              deploy to dev environment"
	@echo "$(purple)deploy-preprod$(end)          deploy to preprod environment"
	@echo "$(purple)deploy-prod$(end)             deploy to prod environment"
 

.PHONY: start
start:
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml up -d

.PHONY: dev-start
dev-start:
	$(DOCKER_COMPOSE_BIN) -f docker-compose.yml up

.PHONY: stop
stop:
	$(DOCKER_COMPOSE_BIN) down

.PHONY: shell-him
shell-him:
	$(DOCKER_BIN) exec -it him bash

.PHONY: bot-run
bot-run:
	$(DOCKER_BIN) exec -it him python manage.py bot

.PHONY: migrate
migrate:
	$(DOCKER_BIN) exec -it him python manage.py migrate

.PHONY: makemigrations
makemigrations:
	$(DOCKER_BIN) exec -it him python manage.py makemigrations

.PHONY: collectstatic
collectstatic:
	$(DOCKER_BIN) exec -it him python manage.py collectstatic

.PHONY: load-fixtures
load-fixtures:
	$(DOCKER_BIN) exec -it him python manage.py loaddata him/fixtures/*.yaml

.PHONY: pip-dev
pip-dev:
	$(DOCKER_BIN) exec -i him pip install -r requirements-dev.txt

.PHONY: codestyle
codestyle:
	$(DOCKER_BIN) exec -i him pip install -r requirements-dev.txt
	$(DOCKER_BIN) exec -i him python -m autoflake --in-place --remove-all-unused-imports -r him/
	$(DOCKER_BIN) exec -i him python -m black him/
	$(DOCKER_BIN) exec -i him python -m isort **/*.py
	sudo chown -R ph:ph .
	
.PHONY: test
test:
	$(DOCKER_BIN) exec -i him coverage run manage.py test
	$(DOCKER_BIN) exec -i him coverage html
	$(DOCKER_BIN) exec -i him coverage-badge -o assets/coverage.svg

.PHONY: cloud_sql_proxy_dev
cloud_sql_proxy_dev:
	cloud_sql_proxy -instances=him:europe-west3:him-dev=tcp:5432

.PHONY: cloud_sql_proxy_preprod
cloud_sql_proxy_preprod:
	cloud_sql_proxy -instances=him:europe-west3:him-preprod=tcp:5432

.PHONY: cloud_sql_proxy_prod
cloud_sql_proxy_prod:
	cloud_sql_proxy -instances=him:europe-west3:him-prod=tcp:5432

.PHONY: build
build:
	gcloud builds submit --config gcp-build.yaml

.PHONY: create-user-dev
create-user-dev:
	gcloud builds submit --config gcp-create-user.yaml --substitutions=_GCP_ENV=dev,_USER_NAME=him,_USER_EMAIL=ph@gleeph.net,_USER_PASSWORD=him

.PHONY: create-user-preprod
create-user-preprod:
	gcloud builds submit --config gcp-create-user.yaml --substitutions=_GCP_ENV=preprod,_USER_NAME=him,_USER_EMAIL=ph@gleeph.net,_USER_PASSWORD=him

.PHONY: create-user-prod
create-user-prod:
	gcloud builds submit --config gcp-create-user.yaml --substitutions=_GCP_ENV=prod,_USER_NAME=him,_USER_EMAIL=ph@gleeph.net,_USER_PASSWORD=N&c%yze5bun7Q2&Zt@kjzbM&62P

.PHONY: deploy-dev
deploy-dev:
	gcloud builds submit --config gcp-deploy.yaml --substitutions=_GCP_ENV=dev

.PHONY: deploy-preprod
deploy-preprod:
	gcloud builds submit --config gcp-deploy.yaml --substitutions=_GCP_ENV=preprod

.PHONY: deploy-prod
deploy-prod:
	gcloud builds submit --config gcp-deploy.yaml --substitutions=_GCP_ENV=prod