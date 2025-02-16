DEPLOY_REGISTRY = ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com
CORE			?= aviso
MODEL			?= full # full , delta Y last
PARAMS			?= null # 267,268 , 1 en dias Y null

sync-config-db:## Sync config-db : make sync-config-db ACCOUNT_ENV=dev
	aws s3 cp s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/config/db-connection.json solr9cores/dataimport/config/ --profile $(ACCOUNT_ENV)
	aws s3 cp s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/config/.env solr9cores/dataimport/ --profile $(ACCOUNT_ENV)

push-config-db:## Sync config-db : make push-config-db ACCOUNT_ENV=dev
	aws s3 cp solr9cores/dataimport/config/db-connection.json s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/config/db-connection.json --profile $(ACCOUNT_ENV)
	aws s3 cp solr9cores/dataimport/.env s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/config/.env --profile $(ACCOUNT_ENV)

sync-core-data-solr: ## Sync data : make sync-core-data-solr ACCOUNT_ENV=dev
	aws s3 sync s3://${INFRA_BUCKET}/config/ec2/${OWNER}/${ENV}/solr/solr9/core/ data/solr9/core/ --profile $(ACCOUNT_ENV)

build-data-import-solr9: ##@Global Create a Docker image with the dependencies packaged
	@docker build -f docker/python310/Dockerfile --no-cache -t $(OWNER)-$(ENV)-dataimport-solr:$(ENV)  docker/python310/

data-import-run:  ##@GDataimport : make data-import-run CORE=santander_profession MODEL=full PARAMS=null
	@make sync-config-db ACCOUNT_ENV=dev;
	docker run -it -e HOME=/app -e AWS_SDK_LOAD_NONDEFAULT_CONFIG=1 \
		-e ENV=dev -e REGION_AWS=$(DEPLOY_REGION) \
		-e AWS_CONFIG_FILE=/app/.aws/config -e AWS_PROFILE=dev -e AWS_SDK_LOAD_CONFIG=1 \
		-v "$(PWD)/solr9cores/dataimport/:/app/dataimport" \
		-v "$(PWD)/solr9cores/$(CORE)/:/app/$(CORE)/conf" \
		-w /app/dataimport \
		-v $(HOME)/.aws/:/app/.aws/:rw \
		--network="$(DOCKER_NETWORK)" \
		$(OWNER)-$(ENV)-dataimport-solr:$(ENV) python3.10 run.py $(CORE) $(MODEL) $(PARAMS)
