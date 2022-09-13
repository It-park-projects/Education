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
from B_authentication.renderers import *
from C_crud.serializers import *
from C_crud.models import *


# Subjects Views
class SubjectsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = Subjects.objects.all()
        serializers = SubjectsList(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = SubjectsList(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
class SubjectsDeteileView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        subject = Subjects.objects.filter(id=pk)
        serializers = SubjectsList(subject,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        serializers = SubjectsList(instance=Subjects.objects.filter(id=pk)[0],data=request.data,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Subjects.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)

# class Group educations
class GroupEducationViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        groups = Education_group.objects.all()
        serializers = EducationGroupSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = EducationGroupSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
class EducationGroupDeteileView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        groups = Education_group.objects.filter(id=pk)
        serializers = EducationGroupSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        serializers = EducationGroupSerializers(instance=Education_group.objects.filter(id=pk)[0],data=request.data,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Education_group.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)

# class Student educations
class StudentEducationViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        groups = Education_students.objects.all()
        serializers = StudentsSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = StudentsSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
class StudentGroupDeteileView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        groups = Education_students.objects.filter(id=pk)
        serializers = StudentsSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        serializers = StudentsSerializers(instance=Education_group.objects.filter(id=pk)[0],data=request.data,partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Education_students.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)