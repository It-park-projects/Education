from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from B_authentication.models import *
from B_authentication.serializers import *
from C_crud.models import *
from dateutil.relativedelta import relativedelta

class SubjectsList(serializers.ModelSerializer):
    teacher_id = CustomUserSerializer(read_only=True)
    education_filial = EduacationFilialSerializers(read_only=True)
    class Meta:
        model = Subjects
        fields = '__all__'
class CreateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['name_subject','price_subject','teacher_id','duration_of_course',]
    def create(self, validated_data):
    
        validated_data['education_filial'] = self.context.get('user_education_filial')
        return super(CreateSubjectSerializer,self).create(validated_data)
    def update(self, instance, validated_data):
        instance.name_subject = validated_data.get('name_subject',instance.name_subject)
        instance.price_subject = validated_data.get('price_subject',instance.price_subject)
        instance.duration_of_course = validated_data.get('duration_of_course',instance.duration_of_course)
        instance.education_filial = self.context.get('user_education_filial')
        instance.teacher_id = validated_data.get('teacher_id',instance.teacher_id)
        # instance.update_date = validated_data.get('update_date',instance.update_date)
        
        instance.save()
        return instance

# Education Groups
class EducationGroupSerializers(serializers.ModelSerializer):
    subject_id = SubjectsList(read_only=True)
    education_main = EduacationMainSerializers(read_only=True)
    education_filial = EduacationFilialSerializers(read_only=True)

    class Meta:
        model = Education_group
        fields = ['name','education_main','education_filial','subject_id', 'id',]
class EducationGroupSerializers1(serializers.ModelSerializer):
    subject_id = SubjectsList(read_only=True)
    
    class Meta:
        model = Education_group
        fields = ['name','subject_id', 'id',]
    
class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education_group
        fields = ['name','subject_id',]
    def create(self, validated_data):
        validated_data['education_filial'] = self.context.get('user_education_filial')
        validated_data['education_main'] = self.context.get('user_education_main')
        return Education_group.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.subject_id = validated_data.get('subject_id',instance.subject_id)
        instance.education_main = self.context.get('user_education_main')
        instance.education_filial = self.context.get('user_education_filial')
        instance.update_date = validated_data.get('update_date',instance.update_date)
        return super().update(instance, validated_data)

# Sudent Serializers
class StudentsSerializers(serializers.ModelSerializer):
    education_main = EduacationMainSerializers(read_only=True)
    education_filial = EduacationFilialSerializers(read_only=True)
    group_id = EducationGroupSerializers(read_only=True,many=True)
    class Meta:
        model = Education_students
        fields = '__all__'
class CreateStudentSerialers(serializers.ModelSerializer):
    class Meta:
        model = Education_students
        fields = ['update_date','group_id','price','address','passort_seria','phone_mother','phone_father','phone','midile_name','last_name','first_name','payment_date','create_date',]
    def create(self, validated_data):
        user_create = Education_students.objects.create(
            first_name = validated_data.get("first_name"),
            last_name = validated_data.get("last_name"),
            midile_name = validated_data.get("midile_name"),
            phone = validated_data.get("phone"),
            phone_father = validated_data.get("phone_father"),
            phone_mother = validated_data.get("phone_mother"),
            passort_seria = validated_data.get("passort_seria"),
            address = validated_data.get("address"),
            price = validated_data.get("price"),
            education_main = self.context.get('user_education_main'),
            education_filial = self.context.get('user_education_filial'),
            create_date = validated_data.get('create_date')
        )
        user_create.payment_date  = validated_data.get('create_date') + relativedelta(months=1)
        print(validated_data['group_id'])
        for i in validated_data['group_id']:
            user_create.group_id.add(i.id)
        user_create.save()
        return  user_create
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
        instance.education_main = self.context.get('user_education_main')
        instance.education_filial = self.context.get('user_education_filial')
        instance.group_id.set(validated_data.get('group_id',instance.group_id)) 
        instance.save()
        return instance
    
class StudentIsDebtorSerializer(serializers.ModelSerializer):
    education_main = EduacationMainSerializers(read_only=True)
    education_filial = EduacationFilialSerializers(read_only=True)
    group_id = EducationGroupSerializers(read_only=True)
    class Meta:
        model = Education_students
        fields = "__all__"
        