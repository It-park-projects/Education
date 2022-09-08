from django.urls import path 
from B_authentication.views import *

urlpatterns = [
    path('all_user/',AllUsers.as_view()),
    path('user_login/',UserLoginViews.as_view()),
    path('user_profile/',UserProfilesView.as_view()),
]