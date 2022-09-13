from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/b_authentication/',include('B_authentication.urls')),
    path('api/c_crud/',include('C_crud.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
