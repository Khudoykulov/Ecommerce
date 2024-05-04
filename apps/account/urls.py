from django.urls import path, include
from .views import (
    UserRegisterAPIView,
    SendEmailAPIView,
    VerifyEmailAPIView,
    LoginAPIView,
    ChangePasswordAPIView,
    ResetPasswordAPIView,
    UserProfileRUDView,
)
from rest_framework.routers import DefaultRouter
app_name = 'account'

# router = DefaultRouter()
# router.register(r'profile', UserViewSet)
urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('send/', SendEmailAPIView.as_view(), name='send'),
    path('verify/', VerifyEmailAPIView.as_view(), name='verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    # path('', include(router.urls))
    path('profile/<int:pk>/', UserProfileRUDView.as_view(), name='user')


]

