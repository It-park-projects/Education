from re import T
from django.db import models
from B_authentication.models import *


class Subjects(models.Model):
    name_subject = models.CharField(max_length=150,null=False,blank=False)
    price_subject = models.CharField(max_length=150,null=False,blank=False)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=False,blank=False)
    teacher_id = models.ForeignKey(CustumUsers,on_delete=models.CASCADE,null=False,blank=False)
    
    def __str__(self):
        return self.name_subject
 
class Education_group(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE, null=False,blank=False) 
    education_main = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=False,blank=False)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=False,blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Education_students(models.Model): 
    parent_tg_id = models.CharField(max_length=50,null=True,blank=False)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    midile_name = models.CharField(max_length=100,null=False,blank=False)
    phone = models.CharField(max_length=100,null=False,blank=False)
    phone_father = models.CharField(max_length=100,null=False,blank=False)
    phone_mother = models.CharField(max_length=100,null=False,blank=False)
    passort_seria = models.CharField(max_length=100,null=False,blank=False)
    address = models.CharField(max_length=100,null=False,blank=False)
    price = models.CharField(max_length=250,null=False,blank=False)
    education_main = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=False,blank=False)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=False,blank=False)
    group_id = models.ForeignKey(Education_group,on_delete=models.CASCADE,null=False,blank=False)
    payment_date = models.DateField(null=True,blank=True)
    create_date = models.DateField()
    update_date = models.DateTimeField(auto_now_add=True)