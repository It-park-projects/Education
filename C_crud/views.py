from rest_framework.response import Response
from rest_framework import status,authentication,permissions
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter,OrderingFilter
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import get_list_or_404
from datetime import datetime,date
from django.utils.dateparse import parse_date
from dateutil.relativedelta import relativedelta
from B_authentication.renderers import *
from C_crud.serializers import *
from C_crud.models import *


# Subjects Views
class SubjectsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = Subjects.objects.filter(education_filial = request.user.education_filial).order_by('-id')
        serializers = SubjectsList(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = CreateSubjectSerializer(data=request.data,context={'user_education_filial':request.user.education_filial})
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
        serializers = CreateSubjectSerializer(instance=Subjects.objects.filter(id=pk)[0],data=request.data,partial=True,context={'user_education_filial':request.user.education_filial})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':'update success'},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Subjects.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)
class TeacherSubjectsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = Subjects.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial,teacher_id = request.user.id)
        serializers = SubjectsList(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class AllFillialTeacherViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['username','first_name','last_name']
    ordering_fields = ['id']
    def get(self,request,format=None):
        users = CustumUsers.objects.filter(groups__name__in = ['Teacher'],education_main=request.user.education_main.id,education_filial = request.user.education_filial).order_by('-pk')
        serializers = CustomUserSerializer(users,many= True)
        return Response(serializers.data,status=status.HTTP_200_OK)

# class Group educations
class GroupEducationViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        groups = Education_group.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial)
        serializers = EducationGroupSerializers(groups, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializers = CreateGroupSerializer(data=request.data,context={'user_education_filial':request.user.education_filial,'user_education_main':request.user.education_main})
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
        serializers = CreateGroupSerializer(instance=Education_group.objects.filter(id=pk)[0],data=request.data,partial=True,context={'user_education_filial':request.user.education_filial,'user_education_main':request.user.education_main})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Education_group.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)
class TeacherGroupViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = Education_group.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial,subject_id__teacher_id = request.user.id)
        serializers = EducationGroupSerializers(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

# class Student educations
class StudentEducationViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        groups = Education_students.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial)
        serializers = StudentsSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = CreateStudentSerialers(data=request.data,context={'user_education_filial':request.user.education_filial,'user_education_main':request.user.education_main})
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
        serializers = CreateStudentSerialers(instance=Education_students.objects.filter(id=pk)[0],data=request.data,partial=True,context={'user_education_filial':request.user.education_filial,'user_education_main':request.user.education_main})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = Education_students.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)
class TeacherStudentViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = Education_students.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial,group_id__subject_id__teacher_id = request.user.id)
        serializers = StudentsSerializers(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class IsDebtorView(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        students = Education_students.objects.filter(education_filial__id_education = request.user.education_main,education_filial = request.user.education_filial).order_by('-pk')
        serializers = StudentIsDebtorSerializer(students,many= True)
        list_debtor = []
        groups = []
        for i in serializers.data:
            if relativedelta(months=1) + date.today() >= parse_date(i['payment_date']):
               
                    how_months_does_not_payed = 0 if not parse_date(i['payment_date']) else relativedelta(parse_date(i['payment_date']),date.today()).months + (12*relativedelta(parse_date(i['payment_date']),date.today()).years) - 1
                    list_debtor.append({
                        'id':i['id'],
                        'full_name':i['first_name']+" "+i['last_name']+" "+i['midile_name'],
                        'is_debtor':'qarzdor',
                        'how_months_does_not_payed':abs(how_months_does_not_payed)
                    })
        return Response({"is_debtor":list_debtor},status=status.HTTP_200_OK)
        