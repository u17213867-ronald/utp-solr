## CONTAINER VARS ##
USERNAME_LOCAL   ?= "$(shell whoami)"
UID_LOCAL        ?= "$(shell id -u)"
GID_LOCAL        ?= "$(shell id -g)"
CONTAINER_NAME   = $(PROJECT_NAME)_backend
IMAGE_DEPLOY_DEV = $(PROJECT_NAME):$(TAG)
APP_DIR          = app
TAG              = 9.2.0

sync-container-config: ##@Local Sync config files from S3
	@make sync-authentication

build-image-solr: ##@Global Create a Docker image with the dependencies packaged
	docker build -f docker/solr$(TAG)/Dockerfile --no-cache -t $(PROJECT_NAME):9.2.1  docker/solr$(TAG)/

build: ##Local Build all required images
	@make config-solr9
	@make build-image-solr
	@make build-data-import-solr9

config-solr9:
	sudo mkdir -p ./data/solr9/core/advertisement/conf && sudo mkdir -p ./data/solr9/core/advertisement/conf/lang && sudo cp -rf ./solr9cores/advertisement/* ./data/solr9/core/advertisement/conf/;
	sudo chmod 777 -R ./data;
	sudo echo -e "#Written by CorePropertiesLocator \n #Tue Apr 04 21:28:42 UTC 2023 \n name=advertisement" > ./data/solr9/core/advertisement/core.properties
	sudo cp -f ./docker/solr$(TAG)/conf/security.json ./data/solr9/core/;

up: ##@Local Start docker container
	@docker compose up -d

down: ##@Local Destroy the project
	@docker rm -f services_solr9

log: ##@Local Show docker container logs
	@docker logs -f services_solr9

migrate: ##@Local Show docker container logs
	@docker 

create-core-solr9: ## Create core: make create-core-solr9 CORE=agencia_ingreso
	docker run --name services_solr9 \
		-e SOLR_AUTH_TYPE=basic  \
		-v "$(pwd)/data/solr9/core:/var/solr/data:rw" \
		-p 8984:8986 \
		-d utp-local-solr:9.2.0 && \
		sleep 60 && \
		docker exec -t services_solr9 /opt/solr/bin/solr create_core -c "${CORE}" -n basic-auth -force && \
		sleep 30 && \
		docker rm -f services_solr9


cp-core-deploy: ## Sync configs files from S3 before to push image to r${ENV}egistry in aws: make sync-config
	aws s3 sync solrcores/ s3://${INFRA_BUCKET}/config/container/${OWNER}/${ENV}/${PROYECT_NAME}/ --profile $(ENV)

push-core-solr9: ## Push configs files from S3 before to push image to r${ENV}egistry in aws: make push-core-solr9 ACCOUNT_ENV=dev
	aws s3 sync solr9cores/ s3://${INFRA_BUCKET}/config/container/${OWNER}/${ENV}/${PROYECT_NAME}/cores/9.2.0/ --profile $(ACCOUNT_ENV)

push-core-data: ## Push data : make push-core-data ACCOUNT_ENV=dev
	aws s3 sync data/solr9/core/ s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/solr9/core/ --profile $(ACCOUNT_ENV);

sync-core-deploy: ## Sync configs files from S3 before to push image to r${ENV}egistry in aws: make sync-config
	aws s3 sync s3://${INFRA_BUCKET}/config/container/${OWNER}/${ENV}/${PROYECT_NAME}/ solrcores/ --profile $(ENV)

sync-authentication:## Sync data : make sync-authentication ACCOUNT_ENV=dev
	aws s3 cp s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/solr9/basicAuth.conf docker/solr9.2.0/conf --profile $(ACCOUNT_ENV)
