from rest_framework.response import Response
from rest_framework import status,authentication,permissions,filters
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import User,Group
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
    def get(self,request,format=None):
        groups = Group.objects.all()
        serializers = GroupSerializer(groups,many=True)
        return Response(serializers.data,status=status.HTTP_201_CREATED)
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
    def delete(self, request,id, *args, **kwargs):
        user=CustumUsers.objects.filter(id=id)
        user.delete()
        return Response({"msg":"user delete"},status=status.HTTP_200_OK)
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
        education_main = Education_filial.objects.filter(id_education=request.user.education_main.id)
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
class AllUsers(GenericAPIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['id']
    def get(self,request,format=None):
        query = self.filter_queryset(CustumUsers.objects.all())
        serializer = CustomUserSerializer(query,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class AllFillialManager(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        users = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger'],education_main=request.user.education_main.id).order_by('-pk')
        serializers = CustomUserSerializer(users,many= True)
        return Response(serializers.data,status=status.HTTP_200_OK)
class AllFillialTeacher(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        users = CustumUsers.objects.filter(groups__name__in = ['Teacher'],education_main=request.user.education_main.id).order_by('-pk')
        serializers = CustomUserSerializer(users,many= True)
        return Response(serializers.data,status=status.HTTP_200_OK)
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
        