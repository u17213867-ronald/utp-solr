import boto3
import json
import datetime
from decouple import config

ENV=config('ENV')
REGION_AWS=config('REGION_AWS')

def conectionLog():
  clientlog = boto3.client('logs',region_name=REGION_AWS)
  groupName='neoauto-%s-solr-dataimport' % ENV
  logStreamName=createStream(clientlog,groupName)
  paramsLogs={
               "clientlog":clientlog,
               "groupName":groupName,
               "logStreamName":logStreamName
             }
  return paramsLogs

def createStream(client,groupName):
  fechaActual=datetime.datetime.now()
  datenow=fechaActual.strftime('%Y%m%d')
  logStreamName='logs-'+datenow
  listLogStream = client.describe_log_streams(logGroupName=groupName,logStreamNamePrefix=logStreamName,orderBy='LogStreamName',descending=True)
  logStreamsExists=False
  for LogStream in listLogStream['logStreams']:
    if LogStream['logStreamName'] == logStreamName:
      logStreamsExists=True
  if (not logStreamsExists):
   print("No existe logstrem se procede a crear")
   try:
     client.create_log_stream(logGroupName=groupName,logStreamName=logStreamName)
   except:
     return logStreamName
  return logStreamName

def structureData(app,function,dih,message,type,traceId):
  data = {
    "type":type,
    "app": app,
    "module": function,
    "message": message,
    "payload": dih,
    "trace": traceId
  }
  return json.dumps(data)

def putlog(params,app,function,dih,message,type,traceId):
  client=params['clientlog']
  data=structureData(app,function,dih,message,type,traceId)
  fechaActual=datetime.datetime.now()
  client.put_log_events(
      logGroupName=params['groupName'],
      logStreamName=params['logStreamName'],
      logEvents=[{'timestamp': int(round(fechaActual.timestamp()* 1000)),'message': data}]
  )