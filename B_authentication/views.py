from rest_framework.response import Response
from rest_framework import status,authentication,permissions,filters
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import api_view,parser_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
from django.shortcuts import get_list_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django.db.models import F
from django.utils.dateparse import parse_date
from B_authentication.models import *
from B_authentication.serializers import *
from B_authentication.renderers import *
from C_crud.serializers import *
from C_crud.models import *
from D_payment.models  import *
from datetime import date 
import json
import pickle


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
        serializers = EduacationFilialSerializers(instance=Education_filial.objects.filter(id=pk)[0],data=request.data,partial =True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)

class AllFillialManager(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    # filter_backends = [SearchFilter,OrderingFilter]
    # search_fields = ['username','first_name','last_name']
    # ordering_fields = ['id']
    def get(self,request,format=None):
        users = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger'],education_main=request.user.education_main.id).order_by('-pk')
        serializers = CustomUserSerializer(users,many= True)
        return Response(serializers.data,status=status.HTTP_200_OK)
class AllFillialTeacher(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    # filter_backends = [SearchFilter,OrderingFilter]
    # search_fields = ['username','first_name','last_name']
    # ordering_fields = ['id']
    def get(self,request,format=None):
        users = CustumUsers.objects.filter(groups__name__in = ['Teacher'],education_main=request.user.education_main.id).order_by('-pk')
        serializers = CustomUserSerializer(users,many= True)
        return Response(serializers.data,status=status.HTTP_200_OK)
        
class ManagerStudetsViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        groups = Education_students.objects.filter(education_filial__id_education = request.user.education_main)
        serializers = StudentsSerializers(groups,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def total_statistics(request):
    today = date.today().month
    total_fillial_manager_user = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger'],education_main=request.user.education_main,education_filial=request.user.education_filial).count()
    total_user = CustumUsers.objects.filter(groups__name__in = ['Fillial Maneger'],education_main=request.user.education_main).count()
    total_teacher_user = CustumUsers.objects.filter(groups__name__in = ['Teachers'],education_main=request.user.education_main).count()
    all_students_total = Education_students.objects.filter(education_main=request.user.education_main).count()
    sums = 0
    total_price = 0
    total_price_fillials = 0
    list_months_statistics = []
    list_months_statistics_fillials = []
    list_months_statistics_fillials1 = []
    for item in PaymentStudent.objects.filter(education_filial__id_education=request.user.education_main):
        sums += int(item.price_payment)
    for k in range(1,today+1,1):
        for l in PaymentStudent.objects.filter(education_filial__id_education=request.user.education_main,payment_date__month = k):
            total_price += int(l.price_payment)
        list_months_statistics.append({'month_id':k,"total_month_price":total_price})

    for t in Education_filial.objects.filter(id_education = request.user.education_main):
        for k in range(1,today+1,1):
            for l in PaymentStudent.objects.filter(education_filial__id=t.id,payment_date__month = k):
                total_price_fillials += int(l.price_payment)    
            list_months_statistics_fillials.append({'month_id':k,"total_month_price":total_price_fillials,'fillial':t.education_name})
        # list_months_statistics_fillials1.append(list_months_statistics_fillials)
    list_statistics = []
    list_statistics.append({
        'fillial_manager':total_fillial_manager_user,
        'total_user':total_user,
        'teacher':total_teacher_user,
        'student':all_students_total,
        'total_price_year':sums,
        'all_price':list_months_statistics,
        'fillial_price':list_months_statistics_fillials1
    })
    return Response({'msg':list(list_statistics)})
        
@api_view(['GET'])
def fillial_statistics(request):
    list_fillials = []
    list_fuck = []
    list_stu = []
    is_debtor_count = []
    list_group = []
    sums_years = 0
    sums_month = 0
    fl = Education_filial.objects.all().filter(id_education = request.user.education_main).values('id')
    for fls in fl.values('id','education_name'):
        list_group = []
        for py in PaymentStudent.objects.filter(education_filial = fls['id'],payment_date__year = date.today().year):
            sums_years += int(py.price_payment)
        for py in PaymentStudent.objects.filter(education_filial= fls['id'],payment_date__month = date.today().month):
            sums_month += int(py.price_payment)
        
        stu = Education_students.objects.filter(education_filial = fls['id']).count()
        gr = Education_group.objects.filter(education_filial = fls['id'])
        for grs in gr.values('id','name','subject_id__price_subject','subject_id__name_subject'):
            stu_count_gr = Education_students.objects.filter(group_id__id = grs['id'])
            grs['oquvchilar_soni'] = stu_count_gr.count()
            list_stu = []
            umumiy_tushum = 0
            for sts in stu_count_gr:
                for pay in PaymentStudent.objects.filter(full_student_name=sts).values('price_payment'):
                    umumiy_tushum += int(pay['price_payment'])
                if relativedelta(months=1) + date.today() >= sts.payment_date:
                    how_months_does_not_payed = 0 if not sts.payment_date else relativedelta(sts.payment_date,date.today()).months + (12*relativedelta(sts.payment_date,date.today()).years) - 1
                    list_stu.append({
                        'name':sts.first_name +" "+sts.last_name,
                        'phone_father':sts.phone_father,
                        'phone_mother':sts.phone_mother,
                        'fillial':sts.education_filial.education_name
                    })
            grs['qarzdorlar_soni'] = len(list_stu)
            grs['umumiy_tushum'] = umumiy_tushum
            list_group.append(grs)
        list_fillials.append({
            "id":fls['id'],
            "filial_nomi": fls['education_name'],
            "oquvchi_soni":stu,
            'yillik_tolov':sums_years,
            'oylik_tolov':sums_month,
            "sertifikat_olgan": 0,
            "sertifikat_olmagan": 0,
            'filial_guruhlari':list_group,
            # 'stu_count_gr':stu_count_gr,
        })
    list_fuck.append({
        'fl_is_debtors':list_stu,
        'fl_is_debtor_count':len(is_debtor_count),
    })
    return Response(list_fillials)

@api_view(['GET'])
def statistics_fl_stu(request):
    list_gr = []
    list_stu = []
    fl = Education_filial.objects.all().filter(id_education = request.user.education_main).values('id')
    for fls in fl.values('id','education_name'):
        fl_gr = Education_group.objects.filter(education_filial = fls['id'])
        for gr in fl_gr:
            fl_stu = Education_students.objects.filter(group_id= gr.id).values('group_id')
            tushishi_kerak_bolgan_summa = 0
            for stu in fl_stu.values("first_name","last_name","midile_name",'group_id',"midile_name","phone","phone_father",'address','price','id','education_filial','education_main'):
                stu["to'lash_kerak"] = (int(stu['price']) * int(gr.subject_id.duration_of_course))
                tushishi_kerak_bolgan_summa += (int(stu['price']) * int(gr.subject_id.duration_of_course))
                sums = 0
                for pay_stu in PaymentStudent.objects.filter(full_student_name = stu['id']):
                    sums += int(pay_stu.price_payment)
                stu["to'lagan_summa"] = sums    
                list_stu.append(stu)
            list_gr.append({
                'id':gr.id,
                'name':gr.name,
                'fl':gr.education_filial.education_name,
                'subject_id':gr.subject_id.name_subject,
                'subject_price':gr.subject_id.price_subject,
                'subject_duration_of_course':gr.subject_id.duration_of_course,
                'tushishi_kerak_bolgan_summa':tushishi_kerak_bolgan_summa,
            })

    return Response({'msg':list(list_gr),'msg1':list(list_stu)})