from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from B_authentication.models import *
from C_crud.models import *
from dateutil.relativedelta import relativedelta

class SubjectsList(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['id','name_subject','price_subject','education_filial','teacher_id']
    def create(self, validated_data):
        return Subjects.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name_subject = validated_data.get('name_subject',instance.name_subject)
        instance.price_subject = validated_data.get('price_subject',instance.price_subject)
        instance.education_filial = validated_data.get('education_filial',instance.education_filial)
        instance.teacher_id = validated_data.get('teacher_id',instance.teacher_id)
        instance.save()
        return instance

# Education Groups
class EducationGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education_group
        fields = ['name','subject_id','education_main','education_filial',]
    def create(self, validated_data):
        return Education_group.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.subject_id = validated_data.get('subject_id',instance.subject_id)
        instance.education_main = validated_data.get('education_main',instance.education_main)
        instance.education_filial = validated_data.get('education_filial',instance.education_filial)
        return super().update(instance, validated_data)

# Sudent Serializers
class StudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education_students
        fields = '__all__'
    def create(self, validated_data):
        user_create = Education_students.objects.create(**validated_data)
        user_create.payment_date = validated_data.get('create_date') + relativedelta(months=1)
        user_create.save()
        return user_create 
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.midile_name = validated_data.get('midile_name',instance.midile_name)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.phone_father = validated_data.get('phone_father',instance.phone_father)
        instance.phone_mother = validated_data.get('phone_mother',instance.phone_mother)
        instance.passort_seria = validated_data.get('passort_seria',instance.passort_seria)
        instance.address = validated_data.get('address',instance.address)
        instance.price = validated_data.get('price',instance.price)
        instance.education_main = validated_data.get('education_main',instance.education_main)
        instance.education_filial = validated_data.get('education_filial',instance.education_filial)
        instance.group_id = validated_data.get('group_id',instance.group_id)
        instance.update_date = validated_data.get('update_date',instance.update_date)
        return instance
    
class StudentIsDebtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education_students
        fields = "__all__"
        