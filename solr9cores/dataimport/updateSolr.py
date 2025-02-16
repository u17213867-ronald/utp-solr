import time
from jdbc_api import conectionMysql,execSQL,execSQLColum,execSQLFull,execSQLProcedureColum,execSQLProcedureFull
from utils.processXML import readFileXML,UpdateMappingFieldXML
from utils.solrApi import setDocuments,conectionSolr,updatejson,cleanCore,cleanCoreDelta,reloadSolrCore
from utils.tools import normalize_list_santanderProfile

def dataimportDelta(mysqlNeoConfig,sql,entityItemXML,core,solrConfig,cn,putlog,dih,traceId):
   putlog(cn,"updateSolr","dataimportDelta",dih,"Inicia dataimport tipo delta","INFO",traceId)
   IdAvisos = eval(dih['params'])
   if len(IdAvisos) == 100:
     msg="cantidad de avisos superior a 100"
     putlog(cn,"updateSolr","dataimportDelta",dih,f"Error {msg}","WARNING",traceId)
     return 400,msg,0

   try:
     columnsTable,dataSQL=execSQL(conectionMysql(mysqlNeoConfig),sql)
   except Exception as error:
     msg="Error de conexion la base de datos MySQL y/o error al ejecutar sql por problema de parametro"
     statusCode=400
     print(error)
     putlog(cn,"updateSolr","dataimportDelta",dih,f'{msg}-{error}',"WARNING",traceId)
     return statusCode,msg,0

   try:
     map=UpdateMappingFieldXML(entityItemXML,columnsTable,cn,putlog,dih,traceId)
     data_solr=setDocuments(dataSQL,map,cn,putlog,dih,traceId)
     solrConn=conectionSolr(core,solrConfig,cn,putlog,dih,traceId)
     cleanCoreDelta(solrConn,cn,putlog,dih,traceId)
     updatejson(solrConn,data_solr,cn,putlog,dih,traceId)
     statusCode=200
     msg="dataimport ejecutado satisfactoriamente"
     amountRecords=len(dataSQL)
     return statusCode,msg,amountRecords
   except Exception as error:
     msg="Error updtae delta"
     statusCode=400
     putlog(cn,"updateSolr","dataimportDelta",dih,f'{msg}-{error}',"WARNING",traceId)
     return statusCode,msg,0
   

def autocompleteFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId):
  try:
     columnsTable=execSQLProcedureColum(conectionMysql(mysqlNeoConfig),sql)
     map=UpdateMappingFieldXML(entityItemXML,columnsTable,cn,putlog,dih,traceId)
     solrConn=conectionSolr("autocomplete",solrConfig,cn,putlog,dih,traceId)
     dataSQL=execSQLProcedureFull(conectionMysql(mysqlNeoConfig),sql)
     data_solr=setDocuments(dataSQL,map,cn,putlog,dih,traceId)
     cleanCore(solrConn,cn,putlog,dih,traceId)
     updatejson(solrConn,data_solr,cn,putlog,dih,traceId)
     msg="dataimport ejecutado satisfactoriamente para el core autocomplete"
     statusCode=200
     return statusCode,msg,len(dataSQL)
  except Exception as error:
     msg="Error en la actualizacion del core autocomplete, modo full"
     statusCode=400
     putlog(cn,"updateSolr","dataimportFull",dih,f'{msg}-{error}',"WARNING",traceId)
     return statusCode,msg,0

def santanderLeadFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId):
  amountRecords=0
  try:
     columnsTable=execSQLColum(conectionMysql(mysqlNeoConfig),sql)
     map=UpdateMappingFieldXML(entityItemXML,columnsTable,cn,putlog,dih,traceId)
     sql = sql + ' LIMIT %d OFFSET %d'
     lim=10100
     ost=0
     solrConn=conectionSolr("lead",solrConfig,cn,putlog,dih,traceId)
     dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
     reloadSolrCore("lead",solrConfig,cn,putlog,dih,traceId)
     cleanCore(solrConn,cn,putlog,dih,traceId)
     while len(dataSQL)>0:
        data_solr=setDocuments(dataSQL,map,cn,putlog,dih,traceId)
        updatejson(solrConn,data_solr,cn,putlog,dih,traceId)
        ost = lim + ost
        amountRecords = len(dataSQL) + amountRecords
        dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
        time.sleep(0.4)
     putlog(cn,"updateSolr","lead",dih,"Fin de Dataimport","INFO",traceId)
     msg="dataimport ejecutado satisfactoriamente para el core lead Full"
     statusCode=200
     return statusCode,msg,amountRecords
  except Exception as error:
     msg="Error en la actualizacion del core lead Full, modo full"
     statusCode=400
     errorMsg=f'{msg}. - Error: {error}'
     putlog(cn,"updateSolr","lead",dih,errorMsg,"WARNING",traceId)
     return statusCode,errorMsg,amountRecords
  
def santanderFinancialProfileFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId):
  amountRecords=0
  try:
     columnsTable=execSQLColum(conectionMysql(mysqlNeoConfig),sql)
     normalize_list_santanderProfile(columnsTable)
     map=UpdateMappingFieldXML(entityItemXML,columnsTable,cn,putlog,dih,traceId)
     sql = sql + ' LIMIT %d OFFSET %d'
     lim=150000
     ost=0
     solrConn=conectionSolr("santander_financial_profile",solrConfig,cn,putlog,dih,traceId)
     dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
     reloadSolrCore("santander_financial_profile",solrConfig,cn,putlog,dih,traceId)
     cleanCore(solrConn,cn,putlog,dih,traceId)
     while len(dataSQL)>0:
        data_solr=setDocuments(dataSQL,map,cn,putlog,dih,traceId)
        updatejson(solrConn,data_solr,cn,putlog,dih,traceId)
        ost = lim + ost
        amountRecords = len(dataSQL) + amountRecords
        dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
     msg="dataimport ejecutado satisfactoriamente para el core Santander Financial Profile Full"
     statusCode=200
     return statusCode,msg,amountRecords
  except Exception as error:
     msg="Error en la actualizacion del core Santander Financial Profile Full, modo full"
     statusCode=400
     errorMsg=f'{msg}. - Error: {error}'
     putlog(cn,"updateSolr","santanderFinancialProfileFull",dih,errorMsg,"WARNING",traceId)
     return statusCode,errorMsg,amountRecords

def dataimportFull(mysqlNeoConfig,sql,entityItemXML,core,solrConfig,cn,putlog,dih,traceId):
   dih['params']=""
   putlog(cn,"updateSolr","dataimportFull",dih,"Inicia dataimport tipo full","INFO",traceId)

   if core=="autocomplete": return autocompleteFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId)
   if core=="santander_financial_profile": return santanderFinancialProfileFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId)
   if core=="lead": return santanderLeadFull(mysqlNeoConfig,sql,entityItemXML,solrConfig,cn,putlog,dih,traceId)

   try:
     columnsTable=execSQLColum(conectionMysql(mysqlNeoConfig),sql)
   except Exception as error:
     msg="Error de conexion la base de datos MySQL, modo full"
     statusCode=400
     print(error)
     putlog(cn,"updateSolr","dataimportFull",dih,f'{msg}-{error}',"WARNING",traceId)
     return statusCode,msg,0
   
   map=UpdateMappingFieldXML(entityItemXML,columnsTable,cn,putlog,dih,traceId)
   sql = sql + ' LIMIT %d OFFSET %d'
   lim=20000
   ost=0
   amountRecords=0

   try:
     solrConn=conectionSolr(core,solrConfig,cn,putlog,dih,traceId)
     dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
     cleanCore(solrConn,cn,putlog,dih,traceId)
     while len(dataSQL)>0:
        data_solr=setDocuments(dataSQL,map,cn,putlog,dih,traceId)
        updatejson(solrConn,data_solr,cn,putlog,dih,traceId)
        ost = lim + ost
        amountRecords = len(dataSQL) + amountRecords
        dataSQL=execSQLFull(conectionMysql(mysqlNeoConfig),sql,lim,ost)
     statusCode=200
     msg="dataimport ejecutado satisfactoriamente"
     return statusCode,msg,amountRecords
   except Exception as error:
    print(error)
    msg="Error update full"
    statusCode=400
    putlog(cn,"updateSolr","dataimportFull",dih,f'{msg}-{error}',"WARNING",traceId)
    return statusCode,msg,0