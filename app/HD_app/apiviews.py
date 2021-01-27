# Imports ---------------------------------------------------
from .models import *
from django.contrib.auth.models import User,Group
from django.core import serializers
from .serializers import *
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

# API -------------------------------------------------------

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
    model = Order2
    queryset = Order2.objects.all()
    serializer_class = OrderSerializer
    serializer_API = OrderSerializerAPI
    
    filterset_fields = {
            'care': ['exact'],
            'document__company_sfk': ['icontains'],
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
    #     # queryset = Order2.objects.all()
    #     serializer = self.serializer_API(self.queryset,many=True, context={'request': request})
    #     return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Order2.objects.all()
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
class DocumentListView(viewsets.ModelViewSet):
    model = Document
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    serializer_API = DocumentSerializerAPI
    
    filterset_fields = {
            'name': ['icontains'],
            'start_date':['gte'],
            'end_date':['lte'],
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
        queryset = Document.objects.all()
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
class DocumentStatusListView(viewsets.ModelViewSet):
    model = DocumentStatus
    queryset = DocumentStatus.objects.all()
    serializer_class = DocumentStatusSerializer
    serializer_API = DocumentStatusSerializerAPI
    
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
        queryset = DocumentStatus.objects.all()
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
    model = Address2
    queryset = Address2.objects.all()
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

