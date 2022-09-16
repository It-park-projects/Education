from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from D_payment.models import *

class StudentPaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model =  PaymentStudent
        fields = '__all__'
    def create(self,validated_data):
        try:
            student = Education_students.objects.get(id = validated_data.get('full_student_name').id)
        except Education_students.DoesNotExist():
            student = None
        plus_one_month = student.payment_date + relativedelta(months=1)
        student_update = Education_students.objects.filter(id = validated_data.get('full_student_name').id).update(payment_date = plus_one_month)
        return PaymentStudent.objects.create(**validated_data)
    def update(self,instance,validated_data):
        instance.full_student_name = validated_data.get('full_student_name', instance.full_student_name )
        instance.price_payment = validated_data.get('price_payment', instance.price_payment )
        instance.payment_date = validated_data.get('payment_date', instance.payment_date )
        instance.save()
        return instance