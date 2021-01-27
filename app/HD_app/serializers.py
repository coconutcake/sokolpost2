# Importy ----------------------------------------------------
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model, authenticate
from HD_app.models import *
from .models import *
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

default_depth = 0
api_depth = 1

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', \
            'groups', 'is_staff', 'is_superuser']
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
class ProfileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileType
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        return ProfileType.objects.create(**validated_data)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)
class ProfileSerializerAPI(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        depth = api_depth

# Serializery -----------------------------------------------
class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'
class OrderTypeSerializerAPI(OrderTypeSerializer):
    class Meta(OrderTypeSerializer.Meta):
        depth = api_depth

class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'
class OrderTypeSerializerAPI(OrderTypeSerializer):
    class Meta(OrderTypeSerializer.Meta):
        depth = api_depth




class OrderSerializer(serializers.ModelSerializer):
    # customer_info = CustomerRelatedField(source='customer', read_only=True)
    # customer = CustomerSerializer(many=False)
    # customer = CustomerSerializer(many=False, read_only=True)
    class Meta:
        model = Order2
        fields = '__all__'
class OrderSerializerAPI(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        depth = api_depth



class ImplementationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementationType
        fields = '__all__'
class ImplementationTypeSerializerAPI(ImplementationTypeSerializer):
    class Meta(ImplementationTypeSerializer.Meta):
        depth = api_depth

class PakietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pakiet
        fields = '__all__'
class PakietSerializerAPI(PakietSerializer):
    class Meta(PakietSerializer.Meta):
        depth = api_depth

class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderStatus
        fields = '__all__'
class OrderStatusSerializerAPI(OrderStatusSerializer):

    class Meta(OrderStatusSerializer.Meta):
        depth = api_depth

class DistanceCalcProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceCalcProfile
        fields = '__all__'
class DistanceCalcProfileSerializerAPI(DistanceCalcProfileSerializer):
    class Meta(DistanceCalcProfileSerializer.Meta):
        depth = api_depth

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'
class DocumentSerializerAPI(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        depth = api_depth

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address2
        fields = '__all__'
class AddressSerializerAPI(AddressSerializer):
    class Meta(AddressSerializer.Meta):
        depth = api_depth

class RateStackSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateStack
        fields = '__all__'
class RateStackSerializerAPI(RateStackSerializer):
    class Meta(RateStackSerializer.Meta):
        depth = api_depth

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = '__all__'
class RateSerializerAPI(RateSerializer):
    class Meta(RateSerializer.Meta):
        depth = api_depth

class DocumentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentStatus
        fields = '__all__'
class DocumentStatusSerializerAPI(DocumentSerializer):
    class Meta(DocumentSerializer.Meta):
        depth = api_depth

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
class MessageSerializerAPI(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        depth = api_depth

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
class UserSettingsSerializerAPI(UserSettingsSerializer):
    class Meta(UserSettingsSerializer.Meta):
        depth = api_depth




# TOKEN ------------------------------------------------------
class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        print(attrs)
        username = attrs.get('username')
        password = attrs.get('password')
    
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = _('Unable to provide')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
    
