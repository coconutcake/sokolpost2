# Adds
from HD_app.additionals.validationprintservice import *
from HD_app.additionals.openfiles import *
import requests
import os
import datetime
import time
import json 
from django.http import QueryDict

def get_current_datetime():
    return datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")


class Subiekt():
    """ Klasa Subiekta"""
    def __init__(self,*args,**kwargs):
        self.cfgpath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'subiektapi.json'))
        self.cfg = JsonFile(self.cfgpath)
    def load_obj(self):
        self.cfg = JsonFile(self.cfgpath)
    def return_obj(self):
        return self.cfg
    def return_json(self):
        return self.cfg.returnJsonFile()
    def get_header(self):
        return self.cfg.returnJsonFile()['header']
    def load_json(self):
        self.json = self.cfg.returnJsonFile()
    def close_obj(self):
        self.cfg.close()
    def get_token(self):
        return self.return_json()['header']['Authorization'].split(" ")[1]
    def get_type(self):
        return "https://" if self.return_json()['https'] == 1 else "http://"
    def get_endpoint(self,name):
        name = name
        endpoint_url = ""
        for x,y in self.return_json().items():
            if x == "urls":
                for h in y:
                    if h['name'] == name:
                        endpoint_url = h['url']    
        self.close_obj()
        return self.return_json()['address']+"/"+endpoint_url
    def custom_endpoint(self,endpoint):
        return self.return_json()['address']+"/"+endpoint
    def get_absolute_endpoint(self,name):
        name = name
        endpoint = self.get_endpoint(name)
        typ = self.get_type()
        self.close_obj()
        #print("{0} - Pełny endpoint do wysyłki: {1}".format(get_current_datetime(),endpoint))
        return typ+endpoint
    def is_subiekt_up(self):
        pass
    def get_status_url(self):
        urls = self.return_json()['urls']
        c = [x['url'] for x in urls if x['name'] == "kontrahenci"]
        #print(c)
    def is_up(self):
        print("{0} - Sprawdzam status subiekta...".format(get_current_datetime()))
        try:
            r = requests.get(self.get_absolute_endpoint("status"),verify=False,timeout=1)
            print("{0} - Subiekt status: {1}".format(get_current_datetime(),r.status_code))
            print("{0} - Subiekt gotowy!".format(get_current_datetime())) if r.status_code == 200 else print("{0} - Subiekt offline!".format(get_current_datetime()))
            return True if r.status_code == 200 else False
        except:
            return False
    
