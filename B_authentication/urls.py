from django.urls import path 
from B_authentication.views import *

urlpatterns = [
    path('all_user/',AllUsers.as_view()),
    path('all_fillial_user/',AllFillialManager.as_view()),  
    path('all_fillial_teacher/',AllFillialTeacher.as_view()),
    path('all_fillial_students/',ManagerStudetsViews.as_view()),
    path('total_statistics/',total_statistics),
    path('user_login/',UserLoginView.as_view()),
    path('user_register/',UserRegisterView.as_view()),
    path('user_profile/',UserProfilesView.as_view()),
    path('user_update/<int:id>/',UserUpdateView.as_view()),
    # path('user_delete/<int:id>/',UserDeleteView.as_view()),
    # path('all_user_delete/',AllUserDeleteView.as_view()),
    path('user_logout_views/',UserLogoutView.as_view()),

    # Education_views
    path('education_views/',EducationViews.as_view()),
    path('education_filial_views/',EducationFilialViews.as_view()),
    path('education_deteilw_views/<int:pk>/',EducationFiliDeteileViews.as_view()),
]