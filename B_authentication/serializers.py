from rest_framework import serializers
from B_authentication.models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustumUsers
        fields = '__all__'