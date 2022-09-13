from django.db import models
from B_authentication.models import *


class Subjects(models.Model):
    name_subject = models.CharField(max_length=150,null=True,blank=True)
    price_subject = models.CharField(max_length=150,null=True,blank=True)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=True,blank=True)
    teacher_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=True,blank=True)
    

class Education_group(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE, null=True,blank=True) 
    education_main = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=True,blank=True)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

class Education_students(models.Model): 
    parent_tg_id = models.CharField(max_length=50,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    midile_name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    phone_father = models.CharField(max_length=100,null=True,blank=True)
    phone_mother = models.CharField(max_length=100,null=True,blank=True)
    passort_seria = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    price = models.CharField(max_length=250,null=True,blank=True)
    education_main = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=True,blank=True)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=True,blank=True)
    group_id = models.ForeignKey(Education_group,on_delete=models.CASCADE,null=True,blank=True)
    payment_date = models.DateField(null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)