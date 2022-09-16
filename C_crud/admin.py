from django.contrib import admin
from C_crud.models import *

@admin.register(Subjects)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name_subject','education_filial','teacher_id',]
    
@admin.register(Education_group)
class Education_groupAdmin(admin.ModelAdmin):
    list_display = ['name',]
    
@admin.register(Education_students)
class Education_studentsAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name',]