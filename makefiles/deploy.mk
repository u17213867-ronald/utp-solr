## DEPLOY VARS ##
BUILD_NUMBER    ?= 000001
BUILD_TIMESTAMP ?= 1560121554
TAG_DEPLOY      ?= $(BUILD_TIMESTAMP).$(BUILD_NUMBER)
ACCOUNT_ID      ?= 929226109038

sync-config-deploy: ## Sync configs files from S3 before to push image to r${ENV}egistry in aws: make sync-config
	aws s3 sync s3://${INFRA_BUCKET}/config/deploy/${OWNER}/${ENV}/${PROYECT_NAME}/ deploy/ --profile $(ENV)

login-aws: ## Run the end to end Tests
	aws ecr get-login-password --region ${DEPLOY_REGION} --profile ${ENV} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com

deploy-list-images: ##@Deploy
	@aws ecr describe-images --region ${DEPLOY_REGION} --repository-name ${PROJECT_NAME} --query 'reverse(sort_by(imageDetails,& imagePushedAt))[:5].imageTags[0]' --output text --profile ${ENV}

permit_schema_solr9:
	@ssh root@${SERVER_SOLR9} 'chown -R solr:solr /opt/${SOLR9_PATH}/${CORE}/conf'

reload-solr9-core:
	@curl --user ${USER}:${PASS} http://${SERVER_SOLR9}:8986/solr/admin/cores?wt=json&action=RELOAD&core=${CORE}

deploy-dataimport:
	@rsync -avz --delete-before solr9cores/${CORE}/* root@${SERVER_SOLR9}:/opt/${SOLR9_PATH}/${CORE}/
	@ssh root@${SERVER_SOLR9} 'cd /opt/${SOLR9_PATH}/${CORE}/;chmod +x deploy.sh;sh deploy.sh $(ENV)'