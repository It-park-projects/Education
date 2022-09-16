from operator import imod
from django.contrib import admin
from D_payment.models import *

@admin.register(PaymentStudent)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['full_student_name',]
