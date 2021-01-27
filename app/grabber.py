from django.conf import settings
import urllib3
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from HD_app.additionals.validationprintservice import *
from HD_app.additionals.subiekt import *
import json
from django.urls import reverse
import requests

# Subiekt
sub = Subiekt()

# endpoints
#accounts_endpoint = sub.cfg_get_absolute_endpoint("accounts")
#accounts_endpoint = "https://172.19.0.3/api/users/"
os.system("curl -X GET -k https://172.19.0.3/api/users/ -H 'Authorization: Token 20011865a6a3a79c47e5fa3b4dd31ba9c490186d' -H 'Accept: application/json'")
#r = requests.get(accounts_endpoint,verify=False)
#r = requests.post(accounts_endpoint,data=json.dumps(data),headers=subiekt.cfg_get_header(),verify=False)
#print(r.status_code)
#print(json.loads(r.content))

