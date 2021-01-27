#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import requests
import json
import time
import os


class db_connect():
    def __init__(self,*args, **kwargs):
        self.cstring = kwargs['cstring']
        print(self.cstring)


connection = mysql.connector.connect(host='mariadb3.iq.pl',
                                        database='gobit_sowa',
                                        user='gobit_sowa',
                                        password='i45bOlCek4161ykxTlpq',
                                        )
connection.set_charset_collation('utf8', 'utf8_general_ci')
cursor = connection.cursor()

conn=db_connect(cstring={'host':'mariadb3.iq.pl'})

