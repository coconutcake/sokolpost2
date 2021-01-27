#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pyodbc 
import requests
import json
import time
import os

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
api_url = "http://192.168.1.10:8000/entry/"
server = '192.168.1.11\INSERTNEXO' 
database = 'Nexo_test' 
username = 'sa' 
password = '' 

# ------------------------------------------------
os.system('clear')
raw_input("\nWcisnij klawisz aby rozpoczac export do API(%s) z %s...\n" % (api_url, server))
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM Nexo_test.ModelDanychContainer.Panstwa;")
columns = [column[0] for column in cursor.description]

data = []

print("Rozpoczynam export do API...")
rekord = 1
for row in cursor.fetchall():
    print("-> Exportuje rekord: %s" % rekord)
    di = dict(zip(columns, row))
    r=requests.post(api_url, data=di)
    if r.status_code == 200:
        print("OK 200")
    else:
        print("Błąd")
    data.append(di)
    rekord = rekord+1

print("Zakończono\n")
raw_input("Wcisnij aby wyjsc...")