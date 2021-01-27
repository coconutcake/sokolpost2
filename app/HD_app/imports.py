# Imports ------------------------------------------
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import ExtractDay
from django.utils.timesince import timesince
from django.core.exceptions import ObjectDoesNotExist
# from .models import *
from django.db.models import F, Func, Avg
from calendar import Calendar
from django.db.models.functions import ExtractYear
# from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.core import serializers
import math
import datetime
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models  import User
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractHour
from .models import *
from django.forms.models import model_to_dict
import json
import ast
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .appconfig import DB, SETTINGS_CWD, APPCONFIG_CWD, DATABASE_CWD
# import mysql.connector
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import date, time, timedelta
from .forms import *
from .serializers import api_depth
from .serializers import *
import time
from rest_framework import status
from django.core import serializers
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, status
from HD_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
# Usunięto z powodu braku kompatybilnosci w django 3.1, dodano ponownie
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ViewSetMixin
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.core.files import File
from openpyxl import load_workbook
from django.db.models import Count
from django.conf import settings
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from dateutil import rrule
from rest_framework.decorators import action
from django.forms import modelformset_factory
from collections import Counter
import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView
from django.contrib import admin
import sys
import requests

# warnings off - Usuwanie warningów przy komunikacji po ssl
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Dodatkowe klasy
from HD_app.additionals.validationprintservice import *
from HD_app.additionals.subiekt import *
from django.test import Client

# Widoki API
from .apiviews import *

# Subiekt obj
subiekt = Subiekt()