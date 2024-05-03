from random import randint

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save, pre_save


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError('Superusers must have an password')
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=123, unique=True)
    full_name = models.CharField(max_length=123, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name or self.email

    def __str__(self):
        return self.email


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    token = models.PositiveIntegerField()
    is_used = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


def user_token_pre_save(sender, instance, *args, **kwargs):
    if not instance.token:
        instance.token = randint(1000, 9999)


pre_save.connect(user_token_pre_save, sender=UserToken)




