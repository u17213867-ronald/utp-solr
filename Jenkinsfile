pipeline {
  agent { label 'master' }
  parameters {
    choice(
            name: 'ENV',
            choices:  "dev\npre\nprod",
            description:  '''dev: Se realiza deploy en el ambiente dev
            pre: Se realiza deploy en el ambiente pre
            prod: Se realiza deploy en el ambiente prod'''
        )
    choice(
      name: 'CORE',
      choices: ['aviso', 'autocomplete', 'lead', 'agencia_ingreso', 'empresa_sunat', 'santander_profession', 'santander_ubigeo', 'santander_financial_profile', 'dataimport'],
      description: '''Seleccionar el core solr a actualizar'''
    )    
  }
  stages {
    stage('Checkout') {
            steps {
                script {
                    wrap([$class: 'BuildUser']) {
                        BUILD_USER_ID = (env.BUILD_USER_ID) ? BUILD_USER_ID : ''
                    }
                }
            }
    }

    stage('Sync Configs') {
      steps {
        script {
          withEnv(["ENV=${ENV}", "INFRA_BUCKET=infraestructura.neoauto.${ENV}"]) {
              sh "make sync-config-deploy"
          }
          def configFile = readYaml file: 'deploy/jenkins.private.yml'
          config = configFile.params
          
          enviromentArray = [
              "ENV=${ENV}",
              "INFRA_BUCKET=${config.INFRA_BUCKET}",
              "DEPLOY_REGION=${config.DEPLOY_REGION}",
              "SERVER_SOLR=${config.SERVER_SOLR}",
              "SOLR_PATH=${config.SOLR_PATH}",
              "CORE=${params.CORE}",
              "SERVER_SOLR9=${config.SERVER_SOLR9}",
              "SOLR9_PATH=${config.SOLR9_PATH}",
              "USER=${config.SOLRUSERGESTION}",
              "PASS=${config.SOLRPASSGESTION}"
          ]
        }
      }
    }

    stage('Update Solr9') {
      stages {
        stage('upload config solr') {
           steps {
               script {
                   if (params.CORE == 'dataimport') {
                       withEnv(enviromentArray) {
                         sh "make deploy-dataimport"
                       }
                   } else {
                       sh "rsync -avz solr9cores/${params.CORE}/* root@${config.SERVER_SOLR9}:/opt/${config.SOLR9_PATH}/${params.CORE}/conf/"
                   }
               }
           }
        }
        stage('Granting Permissions') {
           steps {
             script {
               if (params.CORE != 'dataimport') {
                 withEnv(enviromentArray) {
                   sh 'make permit_schema_solr9'
                 }
               }
             }
           }
        }
        stage('Reload Solr') {
           steps {
             script {
                if (params.CORE != 'dataimport') {
                   withEnv(enviromentArray) {
                     sh "make reload-solr9-core"
                   }
                }
             }
           }
        }
      }
    }

 
  }
  post {
    always {
      cleanWs()
    }
  }
}