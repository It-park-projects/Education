from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from B_authentication.forms import *
from B_authentication.models import *

class NewMyUser(UserAdmin):
    add_form = CreasteUser
    form = ChangeUser
    model = CustumUsers
    list_display = ['username','first_name','last_name',]
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('midile_name','address','phone','passort_seria','price','total_price_persent','education_main','education_filial',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('midile_name','address','phone','passort_seria','price','total_price_persent','education_main','education_filial',)}),
    )
admin.site.register(CustumUsers,NewMyUser)

@admin.register(Education_main)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['education_name']

@admin.register(Education_filial)
class EducationFiliaAdmin(admin.ModelAdmin):
    list_display = ['education_name']

@admin.register(Education_group)
class EducationGroupAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Education_students)
class EducationGroupAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name']