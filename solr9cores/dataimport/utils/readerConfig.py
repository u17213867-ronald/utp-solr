import json

def getConfig(configFile,core):
  try:
   with open(configFile,'r') as config:
     config = json.load(config)
   coreConfig = config[core]
  except FileNotFoundError:
    msgError="No se encuentra el fichero de configuraciones de parametros db-connection.json"
    return msgError,-1
  except KeyError:
    msgError="Nombre de core solr Incorrecto"
    return msgError,-1
  return coreConfig['mysql-neo'],coreConfig['solr']
