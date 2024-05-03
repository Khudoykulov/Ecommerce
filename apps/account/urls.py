from django.urls import path
from .views import UserRegisterAPIView, SendEmailAPIView, VerifyEmailAPIView, LoginAPIView

app_name = 'account'


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('send/', SendEmailAPIView.as_view(), name='send'),
    path('verify/', VerifyEmailAPIView.as_view(), name='verify'),
    path('login/', LoginAPIView.as_view(), name='login'),

]

