from rest_framework.response import Response
from rest_framework import status,authentication,permissions
from rest_framework import permissions, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_list_or_404
from django.http import HttpResponse
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

class UserLoginView(APIView):
    render_classes = [UserRenderers]
    def post(self,request,format=None):
        serializers = UserLoginSerializers(data=request.data, partial=True)
        if serializers.is_valid(raise_exception=True):
            username = serializers.data['username']
            password = serializers.data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({'token':token,'message':'Login success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'none_filed_error':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def post(self,request,format=None):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfilesView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserPorfilesSerializers(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def put(self,request,id,format=None):
        data = request.data
        serializers = UserSerializer(instance=CustumUsers.objects.filter(id=id)[0] ,data=data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({"msg":'Saved'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        
class UserDeleteView(APIView):
    perrmisson_class = [IsAuthenticated]
    def get(self, request,id, *args, **kwargs):
        user=CustumUsers.objects.filter(id=id)
        user.delete()
        return Response({"msg":"user delete"},status=status.HTTP_200_OK)

class AllUserDeleteView(APIView):
    perrmisson_class = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user=CustumUsers.objects.all()
        user.delete()
        return Response({"msg":"all user delete"},status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes  = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


# Education views
class EducationViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        education_main = Education_main.objects.all()
        serializers = EduacationMainSerializers(education_main,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


class EducationFilialViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        education_main = Education_filial.objects.all()
        serializers = EduacationFilialSerializers(education_main,many=True)      
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializers = EduacationFilialSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'Create Sucsess'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
class EducationFiliDeteileViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        education = Education_filial.objects.filter(id=pk)
        serializers = EduacationFilialSerializers(education,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        # education = Education_filial.objects.get(id=pk) 
        serializers = EduacationFilialSerializers(instance=Education_filial.objects.filter(id=pk)[0],data=request.data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)

class AllUsers(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        user = CustumUsers.objects.all()
        serializer = CustomUserSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AllFillialManager(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        user = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger'])
        serializers = CustomUserSerializer(user,many=True)
        list_fillial_user = []
        for i in serializers.data:
            for j in Education_filial.objects.filter(id = i['education_filial']):
                for t in Education_main.objects.filter(id = i['education_main']):
                    list_fillial_user = [{
                        'first_name':i['first_name'],
                        'last_name':i['last_name'] ,
                        'midile_name':i['midile_name'] ,
                        'phone':i['phone'] ,
                        'passort_seria':i['passort_seria'],
                        'address':i['address'] ,
                        'price':i['price'],
                        'total_price_persent':i['total_price_persent'] ,
                        'education_main':t.education_name,
                        'education_filial':j.education_name,
                        'username':i['username'] , 
                    }]
        return Response(list_fillial_user,status=status.HTTP_200_OK)



def total_statistics(request):
    total_manager_user = CustumUsers.objects.filter(groups__name__in = ['Manager']).count()
    total_fillial_manager_user = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger']).count()
    total_teacher_user = CustumUsers.objects.filter(groups__name__in = ['Teachers']).count()
    list_statistics = []
    list_statistics.append({
        'manager':total_manager_user,
        'fillial_manager':total_fillial_manager_user,
        'teacher':total_teacher_user
    })
    return HttpResponse({'msg':list(list_statistics)})
        