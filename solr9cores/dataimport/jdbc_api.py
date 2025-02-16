# -*- coding: utf-8 -*-

import jaydebeapi


def conectionMysql(config):
   conn = jaydebeapi.connect("com.mysql.cj.jdbc.Driver",
                           config['jdbc'],
                           [config['user'], config['pass']],
                           "utils/driver/mysql-connector-j-8.0.33.jar")
   return conn


def execSQL(conection,sql):
  curs = conection.cursor()
  curs.execute(sql)
  columnasTabla=[]
  for colname in curs.description:
    columnasTabla.append(colname[0])
  datos=curs.fetchall()
  conection.close()
  return columnasTabla,datos


def execSQLColum(conection,sql):
  curs = conection.cursor()
  curs.execute(sql)
  columnasTabla=[]
  for colname in curs.description:
    columnasTabla.append(colname[0])
  conection.close()
  return columnasTabla


def execSQLFull(conection,sql,lim,ost):
  curs = conection.cursor()
  curs.execute(sql % (lim, ost))
  datos=curs.fetchall()
  conection.close()
  return datos

def execSQLProcedureColum(conection, query):
  curs = conection.cursor()
  curs.execute(query)
  data = curs.fetchall()
  columnasTabla=[]
  for colname in curs.description:
    columnasTabla.append(colname[0])
  conection.close()
  return columnasTabla


def execSQLProcedureFull(conection,sql):
  curs = conection.cursor()
  curs.execute(sql)
  datos=curs.fetchall()
  conection.close()
  return datos