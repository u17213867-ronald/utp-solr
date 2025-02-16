from bs4 import BeautifulSoup

def readFileXML(xmlFile):
  with open(xmlFile, 'r') as f:
    data = f.read()
  data_xml = BeautifulSoup(data, 'xml')
  return data_xml.find('entity')

def createMappingFieldXML(entityItem):
  #creando el mapping a partir del xml
  mapping=[]
  listAllitemfield=entityItem.find_all('field')
  for item in listAllitemfield:
    mapping.append([item.get('name'),item.get('column'),0])
  return mapping

def UpdateMappingFieldXML(entityItem,columnsTable,cn,putlog,dih,traceId):
  mapping=createMappingFieldXML(entityItem)
  for elem in mapping:
    elem[2]=columnsTable.index(elem[1])
  putlog(cn,"processXML","UpdateMappingFieldXML",dih,"mapping reaizado entre el xml y las columnas del core","INFO",traceId)
  return mapping
