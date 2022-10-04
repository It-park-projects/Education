from django.db import models
from django.contrib.auth.models import AbstractUser
from B_authentication.querysets import group_manager


class Education_main(models.Model):
    education_name = models.CharField(max_length=100,null=True,blank=True)
    address_education = models.CharField(max_length=100,null=True,blank=True)
    logo_education = models.ImageField(upload_to='education_logo/',null=True,blank=True,default=False)
    phone = models.CharField(max_length=100,null=True,blank=True)
    sayt_link = models.URLField(null=True,blank=True)
    payment_date = models.DateField(null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self ):
        return self.education_name

class Education_filial(models.Model):
    education_name = models.CharField(max_length=100,null=True,blank=True)
    address_education = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    id_education = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=True,blank=True)
    payment_date = models.DateField(null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    fl = group_manager.FillialManager()
    
    

    def __str__(self ):
        return self.education_name

class CustumUsers(AbstractUser):
    midile_name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    passort_seria = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    price = models.CharField(max_length=250,null=True,blank=True)
    total_price_persent = models.CharField(max_length=250,null=True,blank=True)
    education_main = models.ForeignKey(Education_main,on_delete=models.CASCADE, null=True,blank=True)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=True,blank=True)



    




    


    


