'''
 systemctl stop flask
 source ./env/bin/activate
 python3.10 run.py autocomplete full ""
'''
import sys
from flask import Flask, jsonify, request
from dataimport_solr import dateimport
from utils.logger import conectionLog,putlog
import uuid


core=sys.argv[1]
mode=sys.argv[2]
params=sys.argv[3]
cn=conectionLog()
traceId=str(uuid.uuid4())
dih={
    'core':core,
    'mode':mode,
    'params':params
}
print(traceId)
putlog(cn,"app","postsolr",dih,"request dataimport init","INFO",traceId)
response = dateimport(dih,putlog,cn,traceId)
print(response)