from django.urls import path
from C_crud.views import *

urlpatterns = [
    # Subjects
    path('subjects_list/',SubjectsViews.as_view()),
    path('teacher_subjects_list/',TeacherSubjectsViews.as_view()),
    path('subjects_detail_view/<int:pk>/',SubjectsDeteileView.as_view()),
    
    # Education groups urls
    path('education_groups_views/',GroupEducationViews.as_view()),
    path('teacher_education_groups_views/',TeacherGroupViews.as_view()),
    path('educ_groups_detail_views/<int:pk>/',EducationGroupDeteileView.as_view()),

    # Education students urls
    path('education_student_views/',StudentEducationViews.as_view()),
    path('teacher_education_student_views/',TeacherStudentViews.as_view()),
    path('is_debtor_student_views/',IsDebtorView.as_view()),
    path('educ_student_detail_views/<int:pk>/',StudentGroupDeteileView.as_view()),
    
    path('fillial_teachers/',AllFillialTeacherViews.as_view()),

    

]