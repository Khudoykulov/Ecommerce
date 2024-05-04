from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str, force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import generics, views, status, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from apps.account.seriallizers import (
    UserRegisterSerializer,
    SendEmailSerializer,
    VerifyEmailSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    # SetNewPasswordSerializer
)
from .models import User, UserToken
from rest_framework.permissions import IsAuthenticated
from .tasks import ecommerce_send_email
from .permissions import IsOwnerOrReadOnly

class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = UserToken.objects.create(user=user)
        ecommerce_send_email.apply_async(('Activation Token Code', token.token, [user.email]), )
        data = {
            'success': True,
            'detail': 'Account created successfully!'
        }
        return Response(data, status=status.HTTP_201_CREATED)


class SendEmailAPIView(generics.GenericAPIView):
    serializer_class = SendEmailSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = UserToken.objects.create(user=user)
        ecommerce_send_email.apply_async(('Activation Token Code', token.token, [user.email]), )
        data = {
            'success': True,
            'detail': 'Account created successfully!'
        }
        return Response(data, status=200)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        obtain_tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(obtain_tokens, status=status.HTTP_200_OK)


class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'datail': 'Your password has been changed',
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.GenericAPIView):   #gmailga habar yuborib beradi
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'datail': 'Your password has been reset',
        }
        return Response(data=data, status=status.HTTP_200_OK)


class UserProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = []

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        data = {
            'success': True,
            'datail': 'Your account has deactivated',
        }
        return Response(data=data, status=status.HTTP_200_OK)




# class PasswordTokenCheckView(generics.GenericAPIView): # kelgan link orqali yangi password yuboriladi
#     serializer_class = ResetPasswordSerializer
#
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             user_id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=user_id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'success': False, 'detail': 'Token is not valid, please try again'}, status=406)
#             return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
#             status=200)
#         except Exception as e:
#             return Response({'success': False, 'detail': f'{e.args}'}, status=401)


# class SetNewPasswordAPIView(views.APIView): # yangi passwordni sax qilamiz
#     def post(self, request, *args, **kwargs):
#         uidb64 = request.data('uidb64')
#         password2 = request.data.get('password2')
#         _id = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(id=_id)
#         user.set_password(password2)
#         user.save()
#         return Response({'success': True, 'message': 'Successfully changed password'}, status=200)
