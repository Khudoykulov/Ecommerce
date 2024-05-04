from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserToken
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=123, write_only=True, validators=[validate_password],
                                      help_text="Enter the same password as")
    password2 = serializers.CharField(max_length=123, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email',
                  'password1', 'password2',]

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(password1)
        user.save()
        return user


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email does not exist')
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.IntegerField()

    class Meta:
        fields = ['email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')
        if UserToken.objects.filter(user__email=email, token=token).exists():
            user_token = UserToken.objects.filter(user__email=email,).last()
            if user_token.is_used:
                raise ValidationError('Verification already exists')
            if token != user_token.token:
                raise ValidationError('Token does not match')
            user_token.is_used = True
            user = User.objects.get(email=email)
            user.is_active = True
            user_token.save()
            user.save()
            return attrs
        raise ValidationError('Email already verified!!!!!!!!!!!')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['password'] = user.password
        token['created_date'] = user.created_date.strftime('%d/%m/%Y')
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, validators=[validate_password])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if self.context['request'].user.check_password(old_password):
            if old_password == password:
                raise ValidationError('Current password does not match!!!!!!!!')
            if password == password2:
                return attrs
            raise ValidationError('Passwords do not match!!!!!')
        raise ValidationError('old password is incorrect!!!!!!!!!!!!')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if self.context['request'].user.check_password(password):
            raise ValidationError('Current password does not match!!!!!!')
        if password == password2:
            return attrs
        raise ValidationError('Current password does not match!!!!')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'avatar', 'is_active',
                  'is_staff', 'is_superuser', 'modified_date', 'created_date']



# class SetNewPasswordSerializer(serializers.Serializer):
#     password1 = serializers.CharField(max_length=123, write_only=True, min_length=6)
#     password2 = serializers.CharField(max_length=123, write_only=True, min_length=6)
#     uidb64 = serializers.CharField(max_length=123, required=True)
#     token = serializers.CharField(max_length=123, required=True)
#
#     class Meta:
#         model = User
#         fields = ('password1', 'password2', 'uidb64', 'token')
#
#     def validate(self, attrs):
#         password1 = attrs.get('password1')
#         password2 = attrs.get('password2')
#         uidb64 = attrs.get('uidb64')
#         token = attrs.get('token')
#         _id = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(id=_id)
#         if not PasswordResetTokenGenerator().check_token(user, token):
#             raise AuthenticationFailed({'success': False, 'detail': 'The reset link is invalid.'})
#         if password1 != password2:
#             raise serializers.ValidationError({'success': False, 'detail': 'Password did not match'})
#         return user


