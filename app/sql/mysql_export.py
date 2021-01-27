#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import requests
import json
import time
import os

os.system('clear')
raw_input("Wcisnij aby podłaczyć...")
connection = mysql.connector.connect(host='mariadb3.iq.pl',
                                        database='gobit_sowa',
                                        user='gobit_sowa',
                                        password='i45bOlCek4161ykxTlpq',
                                        )
connection.set_charset_collation('utf8', 'utf8_general_ci')
api_url = "http://192.168.1.10:8000/entry/"
cursor = connection.cursor()

true_obj = {}

def send_to_api(payload):
    print("Wysyłam id: %s do API... -> %s" % (payload['idf'],api_url))
    r=requests.post(api_url, data=payload)
    if r.status_code == 200:
        print("OK 200")
    else:
        print("Błąd")
    print("\n")

raw_input("Rozpocznij import...")

# Klienci ----------------------------------------------
sql_select_Query = "select * from KLIENCI WHERE Email IS NOT NULL"
q1 = "SELECT KLIENCI.ID_KLIENT, KLIENCI.Nazwa, KLIENCI.Ulica, KLIENCI.Kod_poczt, KLIENCI.Miejscowość,KLIENCI.NIP,KLIENCI.Tel,KLIENCI.Osoba_kontaktowa,KLIENCI.Email,KLIENCI.Tel_kom,UMOWY_SERWISOWE.ID_UMOWA FROM gobit_sowa.KLIENCI LEFT JOIN gobit_sowa.UMOWY_SERWISOWE ON KLIENCI.ID_KLIENT = UMOWY_SERWISOWE.ID_KLIENT WHERE ID_UMOWA IS NOT NULL GROUP BY ID_KLIENT"
q2 = "SELECT KLIENCI.ID_KLIENT, KLIENCI.Nazwa, KLIENCI.Ulica, KLIENCI.Kod_poczt, KLIENCI.Miejscowość,KLIENCI.NIP,KLIENCI.Tel,KLIENCI.Osoba_kontaktowa,KLIENCI.Email,KLIENCI.Tel_kom,UMOWY_SERWISOWE.ID_UMOWA FROM gobit_sowa.KLIENCI LEFT JOIN gobit_sowa.UMOWY_SERWISOWE ON KLIENCI.ID_KLIENT = UMOWY_SERWISOWE.ID_KLIENT WHERE ID_UMOWA IS NOT NULL AND KLIENCI.Email IS NOT NULL GROUP BY ID_KLIENT"
cursor.execute(q1)
data = cursor.fetchall()
columns=[x[0] for x in cursor.description]

for row in data:
    elem = dict(zip(columns, row))
    # print(json.dumps(dict(zip(columns, row)), sort_keys=True, indent=4))
    tel=elem['Tel']
    nip=elem['NIP']
    true_obj['tablef']="KLIENCI"
    true_obj['idf']=elem['ID_KLIENT']

    if elem['Email']:
        try:
            true_obj['email']=elem['Email']
        except:
            pass
    else:
        true_obj['email']=nip.replace('-', '')
    
    true_obj['company_name']=elem['Nazwa']
    
    true_obj['password']="haslodomyslne123"

    try:
        true_obj['phone']=tel.replace(' ', '')
        true_obj['nip']=nip.replace('-', '')
    except:
        pass

    if elem['Osoba_kontaktowa']:
        true_obj['first_name']=elem['Osoba_kontaktowa']
        e = elem['Osoba_kontaktowa']
        person = e.split()

        try:
            true_obj['first_name']=person[0]
        except:
            true_obj['last_name']='brak'

        try:
            true_obj['last_name']=person[1]
        except:
            true_obj['last_name']='brak'

    else:
        true_obj['first_name']='brak'
        true_obj['last_name']='brak'

    # true_obj['city']=elem['Miejscowość'],
    true_obj['postal_code']=elem['Kod_poczt']
    true_obj['cellphone']=elem['Tel_kom']
    true_obj['street']=elem['Ulica']

    send_to_api(true_obj)
    
# ---------------------------------------------------------
if (connection.is_connected()):
    connection.close()
    cursor.close()
    print("MySQL connection is closed")