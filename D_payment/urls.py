from django.urls import path
from D_payment.views import *

urlpatterns = [
    path('payment_list/',PaymentView.as_view()),
    path('payment_detail_view/<int:pk>/',PaymentDetailView.as_view()),
    
]
