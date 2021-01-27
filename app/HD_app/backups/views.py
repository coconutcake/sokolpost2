
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.db.models import Sum
from django.utils.timesince import timesince
from django.core.exceptions import ObjectDoesNotExist
# from .models import *
from django.db.models import F, Func, Avg
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
from django.core.serializers.json import DjangoJSONEncoder
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

# warning off
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Adds
from HD_app.additionals.validationprintservice import *
from HD_app.additionals.subiekt import *
# Subiekt
subiekt = Subiekt()

# API -------------------------------------------------------
class CustomerListView(viewsets.ModelViewSet):
    model = Customer2
    queryset = Customer2.objects.all()
    serializer_class = CustomerSerializer
    
    filterset_fields = {
            'name': ['icontains'],
            'street': ['icontains']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # def list(self, request, *kwargs):
    #     queryset = Customer2.objects.all()
    #     serializer = CustomerSerializerAPI(queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
class MessagesListView(viewsets.ModelViewSet):
    model = Message
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    serializer_API = MessageSerializerAPI
    
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Gdy uruchamiamy glowny adres
    # def list(self, request, *kwargs):
    #     queryset = Message.objects.all()
    #     serializer = MessageSerializerAPI(queryset,many=True, context={'request': request})
    #     return Response(serializer.data)

    # Gdy podajemy id w adresie
    def retrieve(self, request, pk=None):
        queryset = Message.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
    filterset_fields = {
            'username': ['icontains'],
            'is_staff': ['exact']
            }
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
class ProfileTypeViewSet(viewsets.ModelViewSet):
    queryset = ProfileType.objects.all()
    serializer_class = ProfileTypeSerializer
    
    filterset_fields = {
            'name': ['icontains'],
            'description': ['icontains'],
    }
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
class OrderListView(viewsets.ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_API = OrderSerializerAPI
    
    filterset_fields = {
            'care': ['exact'],
            'agreement__company__name': ['icontains'],
            'agreement__company': ['exact'],
            'order_status': ['exact'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)    
class OrderStatusListView(viewsets.ModelViewSet):
    model = OrderStatus
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    serializer_API = OrderStatusSerializerAPI
    
    filterset_fields = {
            'name': ['icontains']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        queryset = OrderStatus.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class OrderTypeListView(viewsets.ModelViewSet):
    model = OrderType
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer
    serializer_API = OrderTypeSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = OrderType.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)    
class ImplementationTypeListView(viewsets.ModelViewSet):
    model = ImplementationType
    queryset = ImplementationType.objects.all()
    serializer_class = ImplementationTypeSerializer
    serializer_API = ImplementationTypeSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = ImplementationType.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)  

class PakietListView(viewsets.ModelViewSet):
    model = Pakiet
    queryset = Pakiet.objects.all()
    serializer_class = PakietSerializer
    serializer_API = PakietSerializerAPI
    filterset_fields = {
            'name': ['icontains'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.',
            'detail': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Pakiet.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)  
class AgreementListView(viewsets.ModelViewSet):
    model = Agreement2
    queryset = Agreement2.objects.all()
    serializer_class = AgreementSerializer
    serializer_API = AgreementSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
            'start_date':['gte'],
            'end_date':['lte'],
            'company':['exact'],
            'pakiet':['exact'],
            'status':['exact']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Agreement2.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)  
class ProfileListView(viewsets.ModelViewSet):
    model = Profile
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    serializer_API = ProfileSerializerAPI
    
    filterset_fields = {
            'user': ['exact'],
            'user__email': ['icontains'],
            'idf': ['exact'],
            'tablef': ['exact'],
            'typ': ['exact'],
            
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)  
class AgreementStatusListView(viewsets.ModelViewSet):
    model = AgreementStatus
    queryset = AgreementStatus.objects.all()
    serializer_class = AgreementStatusSerializer
    serializer_API = AgreementStatusSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
            'description': ['icontains'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = AgreementStatus.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class CompanyListView(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    serializer_API = CompanySerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
            'nip': ['exact'],
            'is_accepted': ['exact'],
            'care': ['exact'],
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Nie udało się utworzyć obiektu z dostarczonych danych',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class DistanceCalcProfileListView(viewsets.ModelViewSet):
    model = DistanceCalcProfile
    queryset = DistanceCalcProfile.objects.all()
    serializer_class = DistanceCalcProfileSerializer
    serializer_API = DistanceCalcProfileSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
            'is_default': ['exact']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = DistanceCalcProfile.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class AddressListView(viewsets.ModelViewSet):
    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    serializer_API = AddressSerializerAPI
    
    filterset_fields = {
            'name':['icontains'],
            'address':['icontains'],
            'company':['exact'],
            'is_default':['exact']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Address.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class RateStackListView(viewsets.ModelViewSet):
    model = RateStack
    queryset = RateStack.objects.all()
    serializer_class = RateStackSerializer
    serializer_API = RateStackSerializerAPI
    
    filterset_fields = {
            'name':['icontains'],
            'rate':['exact']
        }
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            # Account.objects.create_user(**serializer.validated_data)
            serializer.save()
            return Response(
            serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    # def list(self, request, *kwargs):
    #     # queryset = Order.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = RateStack.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data) 
class RateListView(viewsets.ModelViewSet):
    model = Rate
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    
    filterset_fields = {
            'name': ['icontains'],
            'start': ['gte'],
            'stop': ['lte'],
        }
class UserSettingsView(viewsets.ModelViewSet):
    model = UserSettings
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    serializer_API = UserSettingsSerializerAPI
    
    filterset_fields = {
        'user': ['exact'],
        'email_notifications': ['exact']
    }
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Record could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        queryset = UserSettings.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(serializer.data)
    def update(self,request,pk=None):
        queryset = UserSettings.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response({
            'status': 'Bad request',
            'message': 'Record could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
class ServiceOrderView(viewsets.ModelViewSet):
    model = ServiceOrder
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    serializer_API = ServiceOrderSerializerAPI
    
    filterset_fields = {
        'name': ['icontains'],
        'user': ['exact'],
        'no': ['exact'],
        'company': ['exact'],
        'category': ['exact'],
        'care': ['exact'],
        'status': ['exact'],
        'start_datetime': ['exact'],
        'end_datetime': ['exact'],
        'order_type': ['exact'],
        'created_date': ['exact']
    }
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        return Response({
            'status': 'Bad request',
            'message': 'Record could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        queryset = ServiceOrder.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Respose(serializer.data)
class NewsView(viewsets.ModelViewSet):
    model = News
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    serializer_API = NewsSerializerAPI
    
    filterset_fields = {
        'user': ['exact'],
        'name': ['icontains'],
        'created_date': ['exact']
    }
    def retrieve(self,request,pk=None):
        queryset = self.model.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_API(obj, context={'request': request})
        return Response(
            serializer.data
        )



# WIDOKI ----------------------------------------------------

# Zmiana hasła
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'HD_app/change_password.html', {
        'form': form
    })
class MyPasswordResetView(PasswordResetView):
    subject_template_name = 'HD_app/password_reset_subject.txt'
    email_template_name = 'HD_app/password_reset_email.html'
    success_url=reverse_lazy('User_add')
    def get_form_kwargs(self):
        user = get_object_or_404(User, pk=self.kwargs.get('user_pk'))
        return {'data': {'email': user.email}}

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Strona tytułowa 
def home(request):
    printservice = ValidationPrintService("%s: %s" % ("FBV",sys._getframe().f_code.co_name))
    now = datetime.now().month
    template = loader.get_template('HD_app/home.html')
    context = {
        'workers': User.objects.filter(is_staff=True),
        'orders': Order.objects.filter(created_date__month=now)
    }
    printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    if request.method == 'GET':
        printservice.set_request(request)
        printservice.print_get()
        if request.user.is_authenticated:
            printservice.print_green("Wyrzucam widok",".")
            return HttpResponse(template.render(context, request))
        else:
            printservice.print_green("Wyrzucam widok","LOGOWANIE")
            return HttpResponseRedirect(reverse('login'))

    def post(self,request,*args,**kwargs):
        pass

# Klienci
@method_decorator(staff_member_required, name='dispatch')
class CompanyView(LoginRequiredMixin,View):
    """ Widok firmy """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Company_Form
    model = Company
    template_name = 'HD_app/company_add.html'
    template_form = 'HD_app/forms/address_add_form.html'


    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Context
        context = {
            "form": self.form_class,
            "companies": self.model.objects.all(),
            "sub_cfg": subiekt.cfg_return_json(),
            "subiekt_status": subiekt.is_subiekt_up()
        }
    # Return
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_form,{"form":self.form_class})
        return render(request, self.template_name, context)
    
    
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Odbieranie parametrów POST
        user = self.request.POST.get('user') if 'user' in request.POST else None
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
        # zapis firmy
            m = form.save(commit=False)
            m.save()
            ccc = Company.objects.get(pk=m.id)
        # zapis adresu
            adr = Address.objects.create(\
                name="adres",
                nr_dom=form.cleaned_data['nr_dom'],
                nr_lok=form.cleaned_data['nr_lok'],
                city=form.cleaned_data['city'],
                address=form.cleaned_data['ulica'],
                street=form.cleaned_data['ulica'],
                distance=1,
                company=ccc,
                is_default=True
                )
            adr.save()
        # zapis usera
            if form.cleaned_data['is_created_new']:
                u = User.objects.create_user(username=form.cleaned_data['pracownik'],email=form.cleaned_data['pracownik'],password='285u9uh24g2hg938')
                self.printservice.print_green("User","FOUND")
                p = get_object_or_404(Profile,user=u)
                self.printservice.print_green("Profile","FOUND")
                p.company = ccc
                p.save()
                self.printservice.print_green("Profile","SAVED")
            else:
            # user
                if user:
                    try:
                        u = User.objects.get(pk=user)
                        self.printservice.print_green("User","FOUND")
                    except:
                        self.printservice.print_red("User","NOTFOUND")
                    try:
                        p = get_object_or_404(Profile,user=u)
                        self.printservice.print_green("Profile","FOUND")
                    except:
                        self.printservice.print_red("Profile","NOTFOUND")
                    try:
                        p.company = m
                        p.save()
                        self.printservice.print_green("Profile","SAVED")
                    except:
                        self.printservice.print_red("Profile","NOTSAVED")
                else:
                    self.printservice.print_blue("User","SKIPPED")
        # is_sent   
            if form.cleaned_data['is_sent']:
                self.printservice.print_green("Password change?","YES")
                redirect_to = reverse()
                if form.cleaned_data['is_created_new']:
                    redirect_to = reverse("my_password_reset",kwargs={"user_pk":User.objects.get(email=form.cleaned_data['pracownik']).pk})
                else:
                    redirect_to = reverse("my_password_reset",kwargs={"user_pk":user})

                self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
                self.printservice.print_green("Wyrzucam widok",redirect_to)
                return redirect(redirect_to)
            else:
                self.printservice.print_red("Password change?","NO")

            redirect_to = reverse('Company_add')
            self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
            self.printservice.print_green("Wyrzucam widok",redirect_to)
            return redirect(redirect_to)
        else:
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.errors)
            return render(request, self.template_name, {'form': form})      
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDetails(LoginRequiredMixin,UpdateView):
    """ Widok edycji firmy """
    model = Company
    form_class = Company_Form
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).get(\
            request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).post(\
            request, *args, **kwargs)
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Company_add")
    def get_object(self, *args, **kwargs):
        order = get_object_or_404(Company, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDelete(LoginRequiredMixin,DeleteView):
    """ Widok usuwania firmy """
    model = Company
    form_class = Company_Form
    success_url = reverse_lazy('Company_add')
    template_name_suffix = '_delete'




# Company old
@method_decorator(staff_member_required, name='dispatch')
class CompanyView_old(LoginRequiredMixin,View):
    """ Widok firmy """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Company_Form_old
    model = Company
    template_name = 'HD_app/company_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Context
        context = {
            "form": self.form_class,
            "companies": self.model.objects.all()
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Odbieranie parametrów POST
        try:
            user = self.request.POST.get('user') if 'user' in request.POST else None
            self.printservice.print_green("field['user']","RECEIVED") if user else self.printservice.print_red("field['user']","NODATA")
        except:
            self.printservice.print_red("field['user']","FAILED")
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            m = form.save(commit=False)
            m.save()
            if user:
                try:
                    u = User.objects.get(pk=user)
                    self.printservice.print_green("User","FOUND")
                except:
                    self.printservice.print_red("User","NOTFOUND")
                try:
                    p = get_object_or_404(Profile,user=u)
                    self.printservice.print_green("Profile","FOUND")
                except:
                    self.printservice.print_red("Profile","NOTFOUND")
                try:
                    p.company = m
                    p.save()
                    self.printservice.print_green("Profile","SAVED")
                except:
                    self.printservice.print_red("Profile","NOTSAVED")
            else:
                self.printservice.print_blue("User","SKIPPED")

            if form.cleaned_data['is_sent']:
                self.printservice.print_green("Password change?","YES")
                redirect_to = reverse("my_password_reset",kwargs={"user_pk":user})
                self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
                self.printservice.print_green("Wyrzucam widok",redirect_to)
                return redirect(redirect_to)
            else:
                self.printservice.print_red("Password change?","NO")

            redirect_to = reverse('Company_add')
            self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
            self.printservice.print_green("Wyrzucam widok",redirect_to)
            return redirect(redirect_to)
        else:
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.errors)
            return render(request, self.template_name, {'form': form})      
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDetails_old(LoginRequiredMixin,UpdateView):
    """ Widok edycji firmy """
    model = Company
    form_class = Company_Form_old
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).get(\
            request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CompanyViewDetails, self).post(\
            request, *args, **kwargs)
    def get_success_url(self, **kwargs):         
        return reverse_lazy("Company_add")
    def get_object(self, *args, **kwargs):
        order = get_object_or_404(Company, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class CompanyViewDelete_old(LoginRequiredMixin,DeleteView):
    """ Widok usuwania firmy """
    model = Company
    form_class = Company_Form_old
    success_url = reverse_lazy('Company_add')
    template_name_suffix = '_delete'

# Adresy
@method_decorator(staff_member_required, name='dispatch')
class AddressView(LoginRequiredMixin,View):
    """ Widok edycji firmy """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Address_Form
    model = Address
    template_name = 'HD_app/address_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Context
        context = {
            "form": self.form_class,
            "addresses": self.model.objects.all(),
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            form.save()
            redirect_to = reverse('Address_add')
            self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
            self.printservice.print_green("Wyrzucam widok",redirect_to)
            return redirect(redirect_to)
        else: 
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.is_valid())
            print(form.errors)
@method_decorator(staff_member_required, name='dispatch')
class AddressViewDetails(LoginRequiredMixin,UpdateView):
    model = Address
    form_class = Address_Form
    template_name = 'HD_app/address_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AddressViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AddressViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Address_add")

    def get_object(self, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj
@method_decorator(staff_member_required, name='dispatch')
class AddressViewDelete(LoginRequiredMixin,DeleteView):
    model = Address
    form_class = Address_Form
    template_name = 'HD_app/address_delete.html'
    success_url = reverse_lazy('Address_add')
    template_name_suffix = '_delete'

# Użytkownicy
@method_decorator(staff_member_required, name='dispatch')
class UserView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = User_Form
    model = User
    template_name = 'HD_app/user_add.html'
    template_form = 'HD_app/forms/user_add_form.html'
    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "form": self.form_class(),
            "users": self.model.objects.all(),
            "profiles": Profile.objects.all()
            }
        if request.is_ajax():
            if request.method == "GET":
                return render(request,self.template_form,{"form":self.form_class})
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        return render(request,self.template_form,{"form":form})


            
    # Validacja formularza
        form = self.form_class(request.POST)
        tel = request.POST.get('tel')
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            f=form.save(commit=False)
            f.tel = tel
            f.save()
           
            if form.cleaned_data['password_reset']:
                self.printservice.print_green("Password reset?","YES")
                redirect_to = reverse("my_password_reset",kwargs={"user_pk":m.id})
                self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
                self.printservice.print_green("Wyrzucam widok",redirect_to)
                return redirect(redirect_to)
            else:
                self.printservice.print_red("Password change?","NO")

            redirect_to = reverse('User_add')
            self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
            self.printservice.print_green("Wyrzucam widok",redirect_to)
        # Return
            return redirect(redirect_to)
        else: 
            print(form.is_valid())
            print(form.errors)
            return render(request, self.template_name, {'form': form}) 
@method_decorator(staff_member_required, name='dispatch')
class UserViewDetails(LoginRequiredMixin,UpdateView):
    model = User
    profile = Profile
    form_class = User_Form
    template_name = 'HD_app/user_detail.html'
    template_form = 'HD_app/forms/user_detail_form.html'
    template_name_suffix = '_detail'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.is_ajax():
            if request.method == "GET":
                obj = self.get_object() 
                form = self.form_class(instance=obj)
                return render(request,self.template_form,{"form":form})
        return super(UserViewDetails, self).get(\
            request, *args, **kwargs)
        
   
    def post(self, request, *args, **kwargs):
        # self.template_name = self.template_form
        obj = self.get_object()
        form = self.form_class(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({"status":"OK"})
        return render(request,self.template_form,{"form":form})
    
        # self.object = self.get_object()
        # super(UserViewDetails, self).post(\
        #     request, *args, **kwargs)
        
    def get_success_url(self, **kwargs):         
        return reverse_lazy("User_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
    
    def get_profile(self,*args,**kwargs):
        profile = get_object_or_404(self.profile, user__id=self.kwargs['pk'])
        return profile
    
@method_decorator(staff_member_required, name='dispatch')
class UserViewDelete(LoginRequiredMixin,DeleteView):
    model = User
    form_class = User_Form
    template_name = 'HD_app/user_delete.html'
    template_form = 'HD_app/forms/user_delete_form.html'
    success_url = reverse_lazy('User_add')
    template_name_suffix = '_delete'
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"status":"OK"})
        
    def get_object(self,*args,**kwargs):
        return get_object_or_404(self.model,pk=self.kwargs['pk'])

# Profil
@method_decorator(staff_member_required, name='dispatch')
class ProfileViewDetails(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = Profile_Form
    user_form = User_Form
    template_name = 'HD_app/profile_detail.html'
    template_name_suffix = '_detail'
    context_object_name = 'imie'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rq = request.POST
        u = self.get_user_object()
        u.first_name = rq.get('imie')
        u.last_name = rq.get('nazwisko')
        u.email = rq.get('email')
        u.save()
        return super(ProfileViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("User_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
    def get_user_object(self, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=profile.user.pk)
        return user

# Umowy
@method_decorator(staff_member_required, name='dispatch')
class AgreementView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Agreement_Form
    form_class_pakiet = PakietForm
    model = Agreement2
    template_name = 'HD_app/agreement_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
        context = {
            "form": self.form_class,
            "form_pakiet": self.form_class_pakiet,
            "agreements": self.model.objects.all()
        }
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            form.save()
            # return JsonResponse({"status": "OK"})
    # Return
        redirect_to = reverse('Agreement_add')
        self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
        self.printservice.print_green("Wyrzucam widok",redirect_to)
        return redirect(redirect_to)
        # return render(request, self.template_name, {'form': self.form_class})        
@method_decorator(staff_member_required, name='dispatch')
class AgreementViewDetails(LoginRequiredMixin,UpdateView):
    model = Agreement2
    form_class = Agreement_Form
    template_name = 'HD_app/agreement_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AgreementViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Agreement_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class AgreementViewDelete(LoginRequiredMixin,DeleteView):
    model = Agreement2
    form_class = Agreement_Form
    template_name = 'HD_app/agreement_delete.html'
    success_url = reverse_lazy('Agreement_add')
    template_name_suffix = '_delete'

# Zlecenia
@method_decorator(staff_member_required, name='dispatch')
class OrderView(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    form_class = Order_Form
    form_class_template = OrderTemplateForm
    model = Order
    template_name = 'HD_app/order_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
        self.user = self.request.user
    # Context
        context = {
            "form": self.form_class(),
            "form_ordertemplate": self.form_class_template,
            "orders": self.model.objects.all()
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_post()
    # Validacja formularza
        form = self.form_class(request.POST)
        if form.is_valid():
            self.printservice.print_green("Pola formularza","VALID")
            form.save()
        else:
            self.printservice.print_red("Pola formularza","INVALID")
            print(form.errors)
            return render(request, self.template_name, {'form': form})
    # Return
        redirect_to = reverse('Order_add')
        self.printservice.print_green("ReverseURL","FOUND") if redirect_to else self.printservice.print_red("ReverseURL","NOTFOUND")
        self.printservice.print_green("Wyrzucam widok",redirect_to)
        return redirect(redirect_to)
@method_decorator(staff_member_required, name='dispatch')
class OrderViewDetails(LoginRequiredMixin,UpdateView):
    model = Order
    form_class = Order_Form
    template_name = 'HD_app/order_detail.html'
    template_name_suffix = '_detail'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrderViewDetails, self).get(\
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(OrderViewDetails, self).post(\
            request, *args, **kwargs)

    def get_success_url(self, **kwargs):         
        return reverse_lazy("Order_add")

    def get_object(self, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return order
@method_decorator(staff_member_required, name='dispatch')
class OrderViewDelete(LoginRequiredMixin,DeleteView):
    model = Order
    form_class = Order_Form
    template_name = 'HD_app/order_delete.html'
    success_url = reverse_lazy('Order_add')
    template_name_suffix = '_delete'

@method_decorator(staff_member_required, name='dispatch')
class PakietView(View):
    fields = '__all__'
    form_class = PakietForm
    model = Pakiet
    template_name = 'HD_app/pakiet_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "form":self.form_class,
            }
        return render(request,self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            if request.is_ajax():
                 return JsonResponse({"status":"OK"})
            else:
                return redirect(reverse("Pakiet_add"))
        else:
            if request.is_ajax():
                return JsonResponse({"errors":form.errors.as_json()})
            else:
                return render(request, self.template_name, {"form":form,"form_ratestack":form_ratestack})
@method_decorator(staff_member_required, name='dispatch')        
class OrderTemplateView(View):
    fields = '__all__'
    form_class = OrderTemplateForm
    model = OrderTemplate
    template_name = 'HD_app/ordertemplate_add.html'
    def get(self, request, pk=None, *args, **kwargs):
        context = {
            "form":self.form_class,
            }
        return render(request,self.template_name, context)
    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                 return JsonResponse({"status":"OK"})
            else:
                return redirect(reverse("OrderTemplate_add"))
        else:
            if request.is_ajax():
                return JsonResponse({"errors":form.errors.as_json()})
            else:
                return render(request, self.template_name, {"form":form})
        
                


# {JSON}
@staff_member_required
def JSON_load_cares(request):
    """
    Ściąga opiekuna dla podanej firmy. Wykorzystane z Ajaxem do pobierania domyslnego opiekuna firmy po wybraniu pola
    """
    agreement = request.GET.get('agreement',None)
    try:
        a = Agreement2.objects.get(pk=agreement)
        #u = User.objects.get(pk=a.company.care.id)
        u = User.objects.get(pk=request.user.id)
        mo = model_to_dict(u, fields="id")
    except:
        mo = {}
    return JsonResponse(mo, content_type='application/json')
@staff_member_required
def JSON_load_order_template(request):
    """
    Ściąga szablony opisy zlecen
    """
    template_id = request.POST.get('t',None)
    try:
        t = OrderTemplate.objects.get(pk=template_id)
        context = {
            "description": t.description,
            "name": t.name,
            "order_status":t.order_status.id,
            "implementation_type":t.implementation_type.id,
            "order_type":t.order_type.id
        }
    except:
        context = {}
    return JsonResponse(context, content_type='application/json')
@staff_member_required
def JSON_load_addresses(request):
    """
    Ściąga adresy firmy przy zapytaniu o umowe w widoku dodawania zlecenia. Wykorzystane z Ajaxem.
    """
    a = request.GET.get('a',None)
    try:
        ag = Agreement2.objects.get(pk=a)
        ad = Address.objects.filter(company__id=ag.company.id)
        data = ad.values_list("id", flat=True).order_by("id")
        return JsonResponse({"id":list(data)}, content_type='application/json')
    except:
        return JsonResponse({},content_type='application/json')
@staff_member_required
def JSON_rozlicz_zlecenie(request):
    from django.core.serializers.json import DjangoJSONEncoder
    order = request.GET.get('order',None)
    o = Order.objects.get(pk=order)
    s = OrderStatus.objects.get(name="Zrealizowane - rozliczone")
    o.order_status = s
    o.save()
    mo = model_to_dict(o,fields="id,name,order_status,updated_date")
    return JsonResponse(mo, content_type='application/json')
@staff_member_required
def JSON_sumuj_zlecenia(request):
    """
    Sumuj zlecenia danej umowy
    """
    a = request.GET.get('a',None)
    u = request.GET.get('u',None)
    s = request.GET.get('s',None)
    e = request.GET.get('e',None)
    

    start = datetime.now()
    end = datetime.now()
    try:
        start = datetime.strptime(s, "%Y-%m-%d").date()
        end = datetime.strptime(e, "%Y-%m-%d").date()
    except:
        print("Brak dni. listuje z bieżącego miesiąca...")
        start = datetime.today().replace(day=1,hour=0,minute=0,second=0)
        end = datetime.today().replace(month=start.month+1,day=1,hour=0,minute=0,second=0)
        print("od: %s, do: %s" % (start,end))
    
    o = Order.objects.all().filter(agreement__id=a).filter(start_datetime__gte=start, end_datetime__lte=end)
    
    ou = Order.objects.all().filter(agreement__id=a, care__id=u).filter(start_datetime__gte=start, end_datetime__lte=end)
    suma = sum([x.calculate_order() for x in o])
    suma_u = sum([x.calculate_order() for x in ou])
    suma_t = sum([x.calculate_timedelta() for x in o])
    suma_th = sum([(x.calculate_timedelta()/60)/60 for x in o])
    suma_ud = float("{:.2f}".format(sum([x.calculate_order_with_distance() for x in ou])))
    rate = [x.getRateCost() for x in o][0]
    print(suma_ud)
    worker = User.objects.get(pk=u)
    print(worker.id)

    return JsonResponse({"a":int(a),"rate":rate,"suma":suma,"suma_u": suma_u, "suma_ud":suma_ud,"suma_t":suma_t,"suma_th":suma_th,"worker":worker.id}, content_type='application/json')

# SubiektAPI
@method_decorator(staff_member_required, name='dispatch')
class SubiektAPI(LoginRequiredMixin,View):
    """ SubiektAPI """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    def post(self, request, pk=None, *args, **kwargs):
        return self.send_post_to_subiekt(request,pk=None, *args, **kwargs)
    def get_post_data(self,request,exception=None):
        data = {}
        for key, value in request.POST.items():
            if exception:
                if key != exception:
                    data[key] = value
            else:
                data[key] = value
        return data
    def send_post_to_subiekt(self,request,pk=None, *args, **kwargs):
        endpoint = subiekt.cfg_get_absolute_endpoint(request.POST.get('endpoint',''))
        data = self.get_post_data(request,exception="endpoint")
        if subiekt.is_subiekt_up():
            r = requests.post(endpoint,data=json.dumps(data),headers=subiekt.cfg_get_header(),verify=False)
            return JsonResponse({"status": r.status_code,"data": json.loads(r.content)})
        else:
            return JsonResponse({"status": r.status_code,"data": json.loads(r.content)})

# Zestawienia i filtry ----------------------------------

# Filtr Zleceń
@method_decorator(staff_member_required, name='dispatch')
class Raport1View(LoginRequiredMixin,View):
    """ Filtr zleceń """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/raport_order_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # Daty
        try:
            today = datetime.today()
            today2 = datetime.today()+timedelta(days=1)
            begin = today.replace(day=1,month=today.month,year=today.year)
            begin2 = today.replace(day=1,month=today.month,year=today.year)-timedelta(days=1)
            dayss = np.busday_count(begin2.date(),today2.date())
            self.printservice.print_green("Daty","OK")
        except:
            self.printservice.print_red("Daty","FAILED")
    # Q object
        try:
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=begin.date(), end_datetime__date__lte=today.date()))
            self.printservice.print_green("Q object","OK")
        except:
            self.printservice.print_green("Q object","FAILED")
    # Efektywność
        try:
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK")
        except:
            self.printservice.print_red("Efektywność","FAILED")
        self.user = self.request.user
    # Context
        context = {
            "orders": obj,
            "ratestacks": RateStack.objects.all(),
            "rates": Rate.objects.all(),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement_id")]),
            "order_types": OrderType.objects.all(),
            "order_status": OrderStatus.objects.all(),
            "suma":sum([c.calculate_order() for c in obj]),
            "count_orders":len(obj),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "efficiency": None if not 'lis' in locals() else lis
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # Return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
# Filtr zleceń z parametrami
@method_decorator(staff_member_required, name='dispatch')
class Raport1View_filteredByTime(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/raport_order_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # GET
        try:
        # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.GET.items():
                globals()[x] = self.request.GET.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry GET","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja GET
        try:
            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            stt = list(OrderStatus.objects.all().values_list("id",flat=True)) if st == "0" else list(OrderStatus.objects.filter(pk=st).values_list("id",flat=True))
            self.printservice.print_green("Konwersja GET","OK") 
        except:
            self.printservice.print_red("Konwersja GET","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,order_status__id__in=stt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")
    # Printy
        self.printservice.print_green("OrderType",tt)
        self.printservice.print_green("Pracownik",ww)
        self.printservice.print_green("Firma",cc)
        self.printservice.print_green("Start",ss)
        self.printservice.print_green("End",ee)
    # Efektywność
        try:
            today = datetime.today().date()
            dayss = np.busday_count(ss-timedelta(days=1),ee+timedelta(days=1))
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK") 
        except:
            self.printservice.print_red("Efektywność","FAILED")
    # Context
        # OrderStatus (zrealizowane)
        included_status = 6
        context = {
            "orders":obj,
            "suma":sum([c.calculate_order() for c in obj]),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "order_types": OrderType.objects.all(),
            # "companies": Company.objects.all(),
            "count_orders":len(obj),
            "count_orders_completed":len(obj.filter(order_status__pk=included_status)),
            "count_orders_notcompleted":len(obj)-len(obj.filter(order_status__pk=included_status)),
            "order_status":OrderStatus.objects.all(),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement_id")]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in self.model.objects.all()]),
            "efficiency": None if not 'lis' in locals() else lis,
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
        #return render(request, self.template_name, context={"workers": User.objects.filter(is_staff=True),"order_types": OrderType.objects.all()})
# Generator raportu
@method_decorator(staff_member_required, name='dispatch')
class GenerateRaport(LoginRequiredMixin,View):
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    template_name = 'HD_app/order_raport.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.printservice.set_request(request)
        self.printservice.print_get()
    # GET
        try:
        # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.GET.items():
                globals()[x] = self.request.GET.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry GET","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja GET
        try:
            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            aa = list(Agreement2.objects.all().values_list("id",flat=True)) if a == "0" else list(Agreement2.objects.filter(pk=a).values_list("id",flat=True))
            self.printservice.print_green("Konwersja GET","OK") 
        except:
            self.printservice.print_red("Konwersja GET","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")
    # Printy
        self.printservice.print_green("OrderType",tt)
        self.printservice.print_green("Pracownik",ww)
        self.printservice.print_green("Firma",cc)
        self.printservice.print_green("Start",ss)
        self.printservice.print_green("End",ee)
    # Efektywność
        try:
            today = datetime.today().date()
            dayss = np.busday_count(ss-timedelta(days=1),ee+timedelta(days=1))
            hh = 8
            li = [(c.calculate_timedelta()/60)/60 for c in obj]
            li2 = [{"id":c.care.id,"calculated":(c.calculate_timedelta()/60)/60,"suma":c.calculate_order(),"suma_d":c.calculate_order_with_distance()} for c in obj]
            df = pd.DataFrame(li2)
            df2=df.groupby(['id']).sum()
            ddd = df2.to_dict('index')
            df3 = dict()
            fulltime = hh*dayss
            lis = [{'worker':x,'calculated':y['calculated'],'efficiency':(y['calculated']/fulltime)*100,"suma":y['suma'],"suma_d":y['suma_d'],"fulltime":fulltime } for x,y in ddd.items()]
            self.printservice.print_green("Efektywność","OK") 
        except:
            self.printservice.print_red("Efektywność","FAILED")
    # Context
        ordertype_rozliczone = 6
        context = {
            "orders":obj,
            "orders_count":len(obj),
            "suma":sum([c.calculate_order() for c in obj]),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
            "workers": User.objects.filter(is_staff=True,id__in=[obj.values_list("care__id")]),
            "allworkers": User.objects.filter(is_staff=True),
            "order_types": OrderType.objects.filter(id__in=[obj.values_list("order_type__id")]),
            "companies": Company.objects.filter(id__in=[obj.values_list("agreement__company__id")]),
            "agreements": Agreement2.objects.filter(id__in=[obj.values_list("agreement__id")]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
            "efficiency": None if not 'lis' in locals() else lis,
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
        }
        self.printservice.print_green("Context","OK") if context and len(context) > 0 else self.printservice.print_red("Context","FAILED")
    # return
        self.printservice.print_green("Wyrzucam widok",".")
        return render(request, self.template_name, context)
        #return render(request, self.template_name, context={"workers": User.objects.filter(is_staff=True),"order_types": OrderType.objects.all()})
# Rozliczanie
@method_decorator(staff_member_required, name='dispatch')
class AccountOrders(LoginRequiredMixin,View):
    """ Rozliczanie zleceń """
    def __init__(self,*args,**kwargs):
        """ Print object """
        self.printservice = ValidationPrintService("%s: %s" % ("CBV",self.__class__.__name__),"CBV")
    fields = '__all__'
    model = Order
    def get(self,request,pk=None,*args,**kwargs):
        return JsonResponse(request.GET.dict())
    def post(self,request,pk=None,*args,**kwargs):
    # POST
        try:
            # Definiowanie parametrów w zmiennych w pętli
            for x,y in self.request.POST.items():
                globals()[x] = self.request.POST.get(x,None)
                self.printservice.print_green(x,"OK") if globals()[x] != "0" else self.printservice.print_red(x,"ALL")
            self.printservice.print_green("Parametry POST","OK")
        except:
            self.printservice.print_red("Parametry GET","FAILED")
    # Konwersja POST
        try:
            # OrderStatus - wszystkie procz, bedą updatowane
            excluded_status = 6

            today = datetime.today().date()
            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True))
            stt = list(OrderStatus.objects.exclude(pk=excluded_status).values_list("id",flat=True)) if st == "0" else list(OrderStatus.objects.filter(pk=st).values_list("id",flat=True))
            self.printservice.print_green("Konwersja POST","OK") 
        except:
            self.printservice.print_red("Konwersja POST","FAILED") 
    # Q object    
        try:  
            obj = self.model.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,order_status__id__in=stt,agreement__company__id__in=cc))
            self.printservice.print_green("Q object","OK")
            self.printservice.print_green("Orders",[x.id for x in obj])
        except:
            self.printservice.print_green("Q object","FAILED")            
    # Q object override
        try:
            try:
                include_status = 6
                os = OrderStatus.objects.filter(pk=include_status).first()
                self.printservice.print_green("Ordertype","SELECTED")
            except:
                self.printservice.print_red("Ordertype","NOTFOUND")
            obj.update(order_status=os)
            self.printservice.print_green("Order update","OVERIDED")
        except:
            self.printservice.print_red("Order update","FAILED")
    # Return
        return JsonResponse(request.POST.dict())

# Zestawienie Umów
@method_decorator(staff_member_required, name='dispatch')
class Raport2View(LoginRequiredMixin,View):
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_agreement_1.html'
    def get(self, request, pk=None, *args, **kwargs):
        self.user = self.request.user
    # GET
        try:
            print("%s\nOdbieram bane z GET..." % ("-"*30))
            s = self.request.GET.get('s',None)
            e = self.request.GET.get('e',None)
            t = self.request.GET.get('t',None)
            w = self.request.GET.get('w',None)
            c = self.request.GET.get('c',None)
            print("+ OK")
        except:
            print("- Brak danych z GET")
    # Przygotowanie zakresu dat
        try:
            print("%s\nRozpoczynam kalkulacje zakresu dat" % ("-"*30,))
            print("* Obliczanie dni bezweekendowych...")
            today = datetime.today()
            begin = today.replace(day=1,month=today.month,year=today.year)
            dayss = np.busday_count(begin.date(),today.date())
            print("* Zakres dat: %s - %s" % (begin.date(), today.date()))
            print("* Dni bez weekendów: %s" % dayss)
        except:
            print("- Błąd konwersji dat nieweekendowych")
    # Querysets
        orders_u = Order.objects.filter(care__isnull=False).values_list('id', flat=True)
        orders_au = Order.objects.filter(care__isnull=False).values_list('agreement', flat=True)
        orders_uo = Order.objects.filter(care__isnull=False)
        workers_with_orders = User.objects.filter(id__in=orders_u, is_staff=True)
    # Context
        context = {
            "agreements": self.model.objects.all(),
            "orders": Order.objects.all(),
            "companies": Company.objects.all(),
            "workers": User.objects.filter(is_staff=True),
            "czasy" : Order.objects.all().aggregate(diff=Avg(F('end_datetime') - F('start_datetime'))),
            "workers_with_orders": workers_with_orders,
            "orders_u":orders_u,
            "orders_uo":orders_uo,
            "orders_au":orders_au,
            "order_types": OrderType.objects.all(),
            "suma":sum([c.calculate_order() for c in Order.objects.all()]),
            "suma_km_costs":sum([c.calculate_order_with_distance() for c in Order.objects.all()]),
            "suma_km": sum([float(c) for c in Order.objects.all().values_list("address__distance",flat=True) if c]),
            "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
            "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in Order.objects.all()]),
            }
    # Return
        return render(request, self.template_name, context)
# Filtry Umów
@method_decorator(staff_member_required, name='dispatch')
class Agreement1View_filteredByTime(LoginRequiredMixin,View):
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_agreement_1.html'
    def get(self, request, pk=None, *args, **kwargs):

        try:

            s = self.request.GET.get('s',None)
            e = self.request.GET.get('e',None)
            t = self.request.GET.get('t',None)
            w = self.request.GET.get('w',None)
            c = self.request.GET.get('c',None)

            today = datetime.today().date()

            tt = list(OrderType.objects.all().values_list("id",flat=True)) if t == "0" else list(OrderType.objects.filter(pk=t).values_list("id",flat=True))
            ww = list(User.objects.filter(is_staff=True).values_list("id",flat=True)) if w == "0" else list(User.objects.filter(pk=w).values_list("id",flat=True))
            ss = datetime.strptime(s,"%Y-%m-%d").date() if 's' in request.GET and s else today.replace(month=1,day=1)
            ee = datetime.strptime(e, "%Y-%m-%d").date() if 'e' in request.GET and e else today
            cc = list(Company.objects.all().values_list("id",flat=True)) if c == "0" else list(Company.objects.filter(pk=c).values_list("id",flat=True)) 
            
            # Q object
            obj = Order.objects.filter(\
                Q(start_datetime__date__gte=ss, end_datetime__date__lte=ee,care__id__in=ww,order_type__id__in=tt,agreement__company__id__in=cc))
        
            print("-"*30)
            print("Przeszukuje Q...")
            print(obj)
            print("-"*30)
            print("Ordertype: %s" % tt)
            print("Worker: %s" % ww)
            print("Firma: %s" % cc)
            print("Start: %s" % ss)
            print("End: %s" % ee)
            print("-"*30)

            start = ss
            end = ee

            orders_ = obj
            orders_u = obj.values_list('id', flat=True)
            orders_us = obj.values_list('care__id', flat=True)
            orders_au = obj.values_list('agreement', flat=True)
            orders_uo = obj
            agreements_= self.model.objects.filter(id__in=[a.agreement.id for a in orders_])
            #workers_with_orders = User.objects.filter(id__in=orders_u, is_staff=True)
            workers_with_orders = User.objects.filter(id__in=orders_us, is_staff=True)

            print(workers_with_orders)



            context = {
                "workers": User.objects.filter(is_staff=True),
                "workers_a": User.objects.filter(is_staff=True).filter(id__in=[u.id for u in workers_with_orders]),
                "agreements": agreements_,
                "companies": Company.objects.all(),
                "orders": obj,
                "orders_u":orders_u,
                "orders_uo":orders_uo,
                "orders_au":orders_au,
                "workers_with_orders": workers_with_orders,
                "order_types": OrderType.objects.all(),
                "suma":sum([c.calculate_order() for c in obj]),
                "suma_km_costs":sum([c.calculate_order_with_distance() for c in obj]),
                "suma_km": sum([float(c) for c in obj.values_list("address__distance",flat=True) if c]),
                "stawka_km": DistanceCalcProfile.objects.get(is_default=True),
                "suma_czas":sum([(c.calculate_timedelta()/60)/60 for c in obj]),
            }
            return render(request, self.template_name, context)

        except:
            context= {
                "companies": Company.objects.all(),
                "workers": User.objects.filter(is_staff=True),
                "order_types": OrderType.objects.all(),
            }
            return render(request, self.template_name, context)
# Filtry zleceń dla Umowy w czasie
@method_decorator(staff_member_required, name='dispatch')
class OrderAgreement1View_filteredByTime(LoginRequiredMixin,View):
    """
    Widok raportu serwisowego
    """
    fields = '__all__'
    model = Agreement2
    template_name = 'HD_app/raport_order_1_agreement_filteredbytime.html'
    def get(self, request, pk=None, *args, **kwargs):
        try:
            s = self.request.GET.get('s')
            start = datetime.strptime(s, "%Y-%m-%d").date()
            e = self.request.GET.get('e')
            end = datetime.strptime(e, "%Y-%m-%d").date()

            a = self.request.GET.get('a')
            print("Przeszukuje umowe id...: %s" % a)
            agreement = Agreement2.objects.get(pk=a)
            print(agreement)
            
            u = self.request.GET.get('u')
            print("Przeszukuje usera id...: %s" % u)
            worker = User.objects.get(pk=u)
            print(worker)

            print("Przeszukuje zlecenia opikuna: %s, umowy:  %s, w zakresie od: %s, do: %s" % (worker,agreement,start,end))
            orders = Order.objects.filter(care__isnull=False).filter(start_datetime__gte=start, end_datetime__lte=end, care=worker, agreement=agreement)
            print(orders)

            if start != "" and end != "" and u != "" and a != "":
                print("Wyszukuje w zakresie od ... %s > do %s" % (start,end))
                context = {
                    "start":start,
                    "end":end,
                    "agreement":agreement,
                    "worker": worker,
                    "orders":orders
                }
                return render(request, self.template_name, context=context)
                
        except:
            return render(request, self.template_name, context={})


# INNE --------------------------------------------------
class Stats(APIView):

    def get(self, request, format=None):

        current_day = datetime.today()
        current_time = current_day.time()
        start_time = current_time.replace(hour=8, minute=0, second=0)
        end_time = current_time.replace(hour=16, minute=59, second=59)
        complete_shift_start = datetime.combine(current_day.date(), start_time)
        complete_shift_end = datetime.combine(current_day.date(), end_time)
        time_8a = datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0))
        time_8b = datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))

        stan = 'W realizacji'

        shift_times = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00',]

        processing_graph = {
            '08:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '09:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=9, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=9, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '10:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=10, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=10, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '11:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=11, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=11, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '12:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=12, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=12, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '13:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=13, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=13, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '14:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=14, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=14, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '15:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=15, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=15, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '16:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=16, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=16, minute=59, second=59))], order_status__name__icontains=stan).count(),
            
        }
        stan = 'Zrealizowane'
        completed_graph = {
            '08:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=8, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=8, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '09:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=9, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=9, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '10:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=10, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=10, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '11:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=11, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=11, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '12:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=12, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=12, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '13:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=13, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=13, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '14:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=14, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=14, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '15:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=15, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=15, minute=59, second=59))], order_status__name__icontains=stan).count(),
            '16:00': Order.objects.filter(updated_date__range=[datetime.combine(current_day.date(), current_time.replace(hour=16, minute=0, second=0)), datetime.combine(current_day.date(), current_time.replace(hour=16, minute=59, second=59))], order_status__name__icontains=stan).count(),
        }
        
        d = Order.objects.extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        ds = ServiceOrder.objects.extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        s = Order.objects.extra({'x': 'date(start_datetime)'}).values('x').annotate(y=Count('id'))
        ss = ServiceOrder.objects.extra({'x': 'date(start_datetime)'}).values('x').annotate(y=Count('id'))
        e = Order.objects.extra({'x': 'date(end_datetime)'}).values('x').annotate(y=Count('id'))
        p = Order.objects.filter(order_status__name__icontains='W realizacji').extra({'x': 'date(created_date)'}).values('x').annotate(y=Count('id'))
        ptc = Order.objects.filter(created_date__date=datetime.today()).filter(order_status__name__icontains='W realizacji').extra({'x': 'time(created_date)'}).values('x').annotate(y=Count('id'))

        c_order_processing = Order.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], order_status__name__icontains='W realizacji').count()
        
        order_processing = Order.objects.filter(agreement__company__care=request.user, order_status__name__icontains='W realizacji').count()
        order_completed = Order.objects.filter(agreement__company__care=request.user, order_status__name__icontains='Zrealizowane').count()
        c_order_completed = Order.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], order_status__name__icontains='Zrealizowane').count()
        
        cs_order_processing = ServiceOrder.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], status__name__icontains='W realizacji').count()
        csc_order_completed = ServiceOrder.objects.filter(created_date__range=[complete_shift_start, complete_shift_end], status__name__icontains='Zrealizowane').count()

        # Queries
        qs = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date')
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )
        qs1 = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month,
            order_status__name__icontains="W realizacji",
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date'),
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )
        qs2 = Order.objects.filter(\
            updated_date__year=datetime.now().year, 
            updated_date__month=datetime.now().month, 
            order_status__name__icontains="Zrealizowane"
            ).annotate(\
                day=ExtractDay('updated_date'),
                month=ExtractMonth('updated_date')
                ).values(\
                    'day',
                    'month',
                    'updated_date__date'
                    ).annotate(\
                        n=Count('pk')
                        ).order_by(\
                            'day'
                            )

        
        def days_cur_month():
            m = datetime.now().month
            y = datetime.now().year
            ndays = (date(y, m+1, 1) - date(y, m, 1)).days
            d1 = date(y, m, 1)
            d2 = date(y, m, ndays)
            delta = d2 - d1
            return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
        def get_hours():
            import datetime as dt
            hours = [(dt.time(i).strftime('%H:%M')) for i in range(24)]
            return hours
        def make_timeline(days, qs, time_field, value_field):
            timeline1 = {}
            for d in days:
                timeline1.update({d: 0})
                for k in qs:
                    if str(d) == str(k[time_field]):
                        timeline1[d] = k[value_field]
            return timeline1
        
        # Complete timelines
        timeline_month_1 = make_timeline(\
            days=days_cur_month(), 
            qs=qs1, 
            time_field='updated_date__date', 
            value_field='n')
        timeline_month_2 = make_timeline(\
            days=days_cur_month(), 
            qs=qs2, 
            time_field='updated_date__date', 
            value_field='n')
        timeline_month_3 = make_timeline(\
            days=days_cur_month(), 
            qs=qs, 
            time_field='updated_date__date', 
            value_field='n')

        unread_messages = Message.objects.filter(receipt=request.user, is_read=False).count()
        
        # Nie wiem czemu musi tutaj byc import?
        from HD_app.models import Company
        companies_not_accepted = Company.objects.filter(is_accepted=False).count()
        myserviceorders = ServiceOrder.objects.filter(care=request.user, status__name__icontains="W realizacji").count()
        myserviceorders_per_company = ServiceOrder.objects.filter(company__care=request.user, status__name__icontains="W realizacji").count()
        myserviceorders_per_company_zrealizowane = ServiceOrder.objects.filter(company__care=request.user, status__name__icontains="Zrealizowane").count()
        


        output = {
            'orders_created_per_day': d,
            'orders_created_per_start' : s,
            'orders_created_per_end' : e,
            'orders_created_per_time_today': ptc,
            'service_orders_created_per_day': ds,
            'service_orders_created_per_start' : ss,
            'current_day': current_day.date(),
            'current_time': current_time,
            'shift_start_time': start_time,
            'shift_end_time': end_time,
            'shift_start_datetime': complete_shift_start,
            'shift_end_datetime': complete_shift_end,
            'order_td_proccessing': c_order_processing,

            'service_order_td_proccessing': cs_order_processing,
            'service_order_td_completed': csc_order_completed,

            'order_processing': order_processing,
            'order_td_completed': c_order_completed,
            'order_completed': order_completed,
            'processing_graph': processing_graph, 
            'completed_graph': completed_graph,
            'shift_times': shift_times, 
            # 'qs': qs,
            # 'qs2': qs2,
            # 'cm': days_cur_month(),
            'timeline_month_1': timeline_month_1,
            'timeline_month_2': timeline_month_2,
            'timeline_month_3': timeline_month_3,
            'hours': get_hours(),
            'unread_messages': unread_messages,
            'companies_not_accepted': companies_not_accepted,
            'serviceorders_processing': myserviceorders,
            'serviceorders_processing_per_company': myserviceorders_per_company,
            'serviceorders_complated_per_company': myserviceorders_per_company_zrealizowane

        }

        return Response(output)
def mystats(request):
    output = {
        'order_processing': Order.objects.filter(user=request.user, order_status__name__icontains="W realizacji").count(),
        'order_completed': Order.objects.filter(user=request.user, order_status__name__icontains="Zrealizowane").count(),
        'unread_messages': Message.objects.filter(receipt=request.user, is_read=False).count(),
    }
    return JsonResponse(output)

# TOKEN --------------------------------------------------
class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
class CreateTokenView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_staff': user.is_staff
        })

    def get(self, request, *args, **kwargs):
        queryset = Token.objects.get(user=request.user)
        # qs_json = serializers.serialize('json', queryset)
        return Response({"token": str(queryset)})