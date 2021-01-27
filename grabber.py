import os
import requests
import json
import random
import string
import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {"Authorization": "Token 634be2170ebd30e71a4135bfcde247e0807d4171"}
r = requests.get("https://192.168.1.10:4433/api/users/",headers=headers,verify=False)
#print(r.json())

def shuffleupper(string):
    s = 0
    li = []
    for x in string:
        s += 1
        if s % 2 == 0:
            li.append(x.upper())
        else:
            li.append(x.lower())
    return ''.join(li)

def generate_password(length):
    letters = shuffleupper(string.ascii_lowercase)
    numbers = random.randrange(1000,9999)
    result_str = ''.join(random.choice(letters) for i in range(length))
    raw_passwd = result_str+str(numbers)
    li = ''.join(random.choice(raw_passwd) for i in range(length))
    return li[:length]

accounts = [
    {
        "id":x.get("id",None),
        "email":x.get("email",""),
        "password":(generate_password(10))
        } for x in r.json()
    ]



print(("Wynik").center(60,"."))
pprint.pprint(accounts)
 