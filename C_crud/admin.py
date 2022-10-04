from django.contrib import admin
from C_crud.models import *

@admin.register(Subjects)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name_subject','education_filial','teacher_id',]
    
@admin.register(Education_group)
class Education_groupAdmin(admin.ModelAdmin):
    list_display = ['name',]
    
# @admin.register(Education_students)
class Education_studentsAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','get_name',]

    def get_name(self, obj):
        return obj.education_filial.education_name
    get_name.admin_order_field  = 'education_filial__education_name'
    get_name.short_description = 'Education Name'
admin.site.register(Education_students,Education_studentsAdmin)