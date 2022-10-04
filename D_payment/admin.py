from operator import imod
from django.contrib import admin
from D_payment.models import *

# @admin.register(PaymentStudent)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['get_name',]
    def get_name(self, obj):
        return obj.full_student_name.first_name
    get_name.admin_order_field  = 'full_student_name__first_name'
    get_name.short_description = 'Author Name'
admin.site.register(PaymentStudent,PaymentAdmin)