from rest_framework import serializers
from B_authentication.models import *

class UserLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    class Meta:
        model = CustumUsers
        fields = ['username','password',]
class UserPorfilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'