from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from D_payment.serializers import *
from D_payment.models import *


class PaymentView(APIView):
    # render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    def get(self,request,format=None):
        subjects = PaymentStudent.objects.all()
        
        serializers = StudentPaymentSerializers(subjects,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def  post(self,request,format=None):
        serializers = StudentPaymentSerializers(data=request.data,context = {'user_education_filial':request.user.education_filial})
        if serializers.is_valid(raise_exception=True):
            serializers.save() 
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    perrmisson_class = [IsAuthenticated]
    def get(self,request,pk,format=None):
        subject = PaymentStudent.objects.filter(id=pk)
        serializers = StudentPaymentSerializers(subject,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        serializers = StudentPaymentSerializers(instance=PaymentStudent.objects.filter(id=pk)[0],data=request.data,partial=True,context = {'user_education_filial':request.user.education_filial})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message':"success update date"},status=status.HTTP_200_OK)
        return Response({'error':'update error data'},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        subject = PaymentStudent.objects.get(id=pk)
        subject.delete()
        return Response({'message':'delete success'},status=status.HTTP_200_OK)
    
    
    