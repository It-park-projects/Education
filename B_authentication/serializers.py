from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from B_authentication.models import *
from django.contrib.auth.models import Group

class UserLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    
    class Meta:
        model = CustumUsers
        fields = ['username','password',]

class EduacationMainSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education_main
        fields = ['id','education_name','address_education','phone',]

    def create(self, validated_data):
        return Education_main.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.education_name = validated_data.get('education_name',instance.education_name)
        instance.address_education = validated_data.get('address_education',instance.address_education)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.save() 
        return instance()

class EduacationFilialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education_filial
        fields = ['id','education_name','address_education','id_education','phone',]

    def create(self, validated_data):
        return Education_filial.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.education_name = validated_data.get('education_name',instance.education_name)
        instance.address_education = validated_data.get('address_education',instance.address_education)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.id_education = validated_data.get('id_education',instance.id_education)
        instance.save() 
        return instance
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = CustumUsers
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        return super(UserSerializer, self).create(validated_data)
    
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.username))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.midile_name = validated_data.get('midile_name', instance.midile_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.passort_seria = validated_data.get('passort_seria', instance.passort_seria)
        instance.address = validated_data.get('address', instance.address)
        instance.price = validated_data.get('price', instance.price)
        instance.total_price_persent = validated_data.get('total_price_persent', instance.total_price_persent)
        instance.education_main = validated_data.get('education_main', instance.education_main)
        instance.education_filial = validated_data.get('education_filial', instance.education_filial)
        instance.groups.set(validated_data.get('groups', instance.groups))
        
        instance.save()
        return instance

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserPorfilesSerializers(serializers.ModelSerializer):
    education_main = EduacationMainSerializers(read_only=True)
    groups = GroupSerializer(read_only=True, many=True)
    class Meta:
        model = CustumUsers
        fields = ['username','id','groups','first_name','last_name','education_main',]

class CustomUserSerializer(serializers.ModelSerializer):
    # education_filial = serializers.ReadOnlyField(source='education_filial.education_name')
    education_main = EduacationMainSerializers(read_only=True)
    # ManyToMany dan faqat bita fields ni uqiydi
    # groups = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='name',
    # )
    groups = GroupSerializer(read_only=True, many=True)
    education_filial = EduacationFilialSerializers(read_only=True)
    # def get_groups(self, obj):
    #     return obj.groups.values_list('name', flat=True)
    class Meta:
        model = CustumUsers
        fields = ['id','username','groups','first_name','last_name','midile_name','phone','passort_seria','address','price','total_price_persent','education_main','education_filial',]
    # def to_internal_value(self, data):
    #     try:
    #         try:
    #             obj_id = data['id']
    #             return CustumUsers.objects.get(id=obj_id)
    #         except KeyError:
    #             raise serializers.ValidationError(
    #                 'id is a required field.'
    #             )
    #         except ValueError:
    #             raise serializers.ValidationError(
    #                 'id must be an integer.'
    #             )
    #     except CustumUsers.DoesNotExist:
    #         raise serializers.ValidationError(
    #         'Obj does not exist.'
    #         )
    
