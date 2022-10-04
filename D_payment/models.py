from django.db import models
from B_authentication.models import *
from C_crud.models import *

class PaymentStudent(models.Model):
    full_student_name = models.ForeignKey(Education_students,on_delete=models.CASCADE,null=False,blank=True)
    price_payment = models.CharField(max_length=250,null=False,blank=True)
    payment_date = models.DateField(null=False,blank=True)
    education_filial = models.ForeignKey(Education_filial,on_delete=models.CASCADE, null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True,blank=True)
    
    def __str__(self ):
        return self.price_payment