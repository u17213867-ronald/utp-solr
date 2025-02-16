from flask import Flask, jsonify, request
from dataimport_solr import dateimport
from utils.logger import conectionLog,putlog
import uuid

app = Flask(__name__)

@app.route('/solr/health',methods=['GET'])
def health():
  return jsonify({"status":200,"message":"Ok"}),200

@app.route('/solr/dataimport', methods=['POST'])
def postsolr():
    cn=conectionLog()
    traceId=str(uuid.uuid4())
    dih={
       'core':request.json['core'],
       'mode':request.json['mode'],
       'params':request.json['customParameters']
    }
    putlog(cn,"app","postsolr",dih,"request dataimport init","INFO",traceId)
    messages=dateimport(dih,putlog,cn,traceId)
    response={
      "status":messages['status'],
      "message":messages['message'],
      "indexed documents":messages['idx'],
      "trace":traceId,
      "cloudwatch":f"{cn['groupName']}|{cn['logStreamName']}"
    }
    return jsonify(response),messages['status']

## Inicializando funcion main de la API
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8985,debug=False)