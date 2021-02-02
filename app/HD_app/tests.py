from django.test import TestCase, Client
import json
import requests
from HD_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from django.forms.models import model_to_dict
print("\n")

# Testy --------------------------------------------------------
