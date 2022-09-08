from rest_framework.response import Response
from rest_framework import status,authentication,permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from B_authentication.models import *
from B_authentication.serializers import *
from B_authentication.renderers import *

# token Olish
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'accsess':str(refresh.access_token)
    }

class AllUsers(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        all_user = CustumUsers.objects.all()
        ser = CustomUserSerializer(all_user,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)