.DEFAULT_GOAL := help
.PHONY: venv
.EXPORT_ALL_VARIABLES:

## APP VARS ##
OWNER           = utp
PROYECT_NAME	= solr
ACCOUNT_ID      ?= 558705146899
DEPLOY_REGION   ?= us-east-1
DOCKER_NETWORK	?= utp_network
## GENERAL VARS ##
ENV             ?= local
INFRA_BUCKET    ?= infraestructura.utp.local
PROJECT_NAME    = $(OWNER)-$(ENV)-$(PROYECT_NAME)
APP_DIR         = app
ACCOUNT_ENV		?= ${ENV}

## INCLUDE TARGETS ##
include makefiles/container.mk
include makefiles/deploy.mk
include makefiles/dataimport.mk
include makefiles/help.mk