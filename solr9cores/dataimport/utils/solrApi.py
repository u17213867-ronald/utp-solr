import pysolr
import requests
from decouple import config as cf
from requests.auth import HTTPBasicAuth

def setDocuments(dataSQL_import,mappingDataConfig,cn,putlog,dih,traceId):
  data_solr=[]
  for data in dataSQL_import:
    document={}
    for elemt in mappingDataConfig:
      document[elemt[0]]=data[elemt[2]]
    data_solr.append(document)
  putlog(cn,"solrApi","setDocuments",dih,"Se adecua la data mysql a las columnas del core de acuerdo al maping realizado","INFO",traceId)
  return data_solr

def conectionSolr(core,config,cn,putlog,dih,traceId):
  urlsolrUpdate='http://{}:{}/solr/{}/'.format(config['host'], config['port'], core)
  tiempoMuerto=config['timeout']
  solr = pysolr.Solr(urlsolrUpdate,always_commit=True,timeout=tiempoMuerto,auth=HTTPBasicAuth(config['user'],config['pass']))
  putlog(cn,"solrApi","conectionSolr",dih,"Conexion solr","INFO",traceId)
  return solr

def reloadSolrCore(core,config,cn,putlog,dih,traceId):
  try:
     url = f"http://{config['host']}:{config['port']}/solr/admin/cores?action=RELOAD&core={core}"
     response = requests.get(url, auth=(cf('ADM_USER'),cf('ADM_PASS')))
     response.raise_for_status() 
     print(f"Core {core} reloaded successfully.")
     putlog(cn,"solrApi","reloadSolrCore",dih,"reload core","INFO",traceId)
  except requests.exceptions.HTTPError as err:
     msgError=f"Failed to reload core {core}. Error message: {err}"
     print(msgError)
     putlog(cn,"solrApi","reloadSolrCore",dih,msgError,"WARNING",traceId)

def cleanCore(solr,cn,putlog,dih,traceId):
  solr.delete(q='*:*')
  putlog(cn,"solrApi","cleanCore",dih,"Se elimina todos los documentos solr","INFO",traceId)

def cleanCoreDelta(solr,cn,putlog,dih,traceId):
  IdAvisos=eval(dih['params'])
  for id in IdAvisos:
    solr.delete(q=f'advertisementId:{id}')
  putlog(cn,"solrApi","cleanCoreDelta",dih,"Se elimina documentos solr de acuerdo a lo encontrado en mysql","INFO",traceId)
  

def updatejson(solr,data_solr,cn,putlog,dih,traceId):
  solr.add(data_solr)
  putlog(cn,"solrApi","updatejson",dih,f"Se agrega {len(data_solr)} documentos a solr","INFO",traceId)