# -*- coding: utf-8 -*-

from utils.readerConfig import getConfig
from utils.processXML import readFileXML
from updateSolr import dataimportDelta,dataimportFull
import datetime

def dateimport(dih,putlog,cn,traceId):
 core=dih['core']
 mode=dih['mode']
 pathDataConfig='../%s/conf/data-config.xml' % core
 mysqlNeoConfig,solrConfig=getConfig('config/db-connection.json',core,)

 if solrConfig==-1:
  msg=mysqlNeoConfig
  statusCode=400
  putlog(cn,"dataimport_solr","dataimport",dih,f"Error {solrConfig}","WARNING",traceId)
  return {"status":statusCode,"message":msg,"idx":"Error no se indexo"}

 try:
   entityItemXML=readFileXML(pathDataConfig)
 except FileNotFoundError:
   msg="No se encuentra el fichero de configuracion del dataimport data-config.xml"
   statusCode=400
   putlog(cn,"dataimport_solr","dataimport",dih,f"Error {msg}","WARNING",traceId)
   return {"status":statusCode,"message":msg,"idx":"Error no se indexo"}

 if mode=="full":
   sql=entityItemXML.get('fullQuery')
   delta=0
 elif mode=="delta":
   sql=entityItemXML.get('deltaImporQuery').format(delta_id=dih['params'])
   delta=1
 elif mode=="last":
   dias=dih['params']
   fechaActual = datetime.datetime.now()
   try:
    delta = datetime.timedelta(days=int(dias))
   except ValueError:
    msg="Este parametro representa un numero entero de días, por favor ingresar un numero entero"
    putlog(cn,"dataimport_solr","dataimport",dih,f"Error {msg}","WARNING",traceId)
    return {"status":400,"message":msg,"idx":"Error no se indexo"}
   fechaInicial = fechaActual - delta
   fechaInit = fechaInicial.strftime('%Y-%m-%d 00:00:00')
   sql=entityItemXML.get('lastImportQuery').format(last_time=fechaInit)
   delta=1
 else:
   sql="El modo de dataimport fue incorrectamenete ingresado"
   putlog(cn,"dataimport_solr","dataimport",dih,f"Error {sql}","WARNING",traceId)
   return {"status":400,"message":sql,"idx":"Error no se indexo"}

 if delta==1:
     statusCode,msg,amountRecords = dataimportDelta(mysqlNeoConfig,sql,entityItemXML,core,solrConfig,cn,putlog,dih,traceId)
 else:
     statusCode,msg,amountRecords = dataimportFull(mysqlNeoConfig,sql,entityItemXML,core,solrConfig,cn,putlog,dih,traceId)
 putlog(cn,"dataimport_solr","dataimport",dih,f'{msg} - {amountRecords} documentos actualizados',"INFO" if statusCode==200 else "WARNING",traceId)
 return {"status":statusCode,"message":msg,"idx":amountRecords}