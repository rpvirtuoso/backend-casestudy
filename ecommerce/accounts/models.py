from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from product.models import Customer


# Create your models here.

class MyAccountManger(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(email=self.normalize_email(email), name=name, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=self.normalize_email(email), name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = MyAccountManger()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# for account in Account.objects.all():
#     Token.objects.get_or_create(user=account)
#
#
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        print('Created using decorator')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender,instance=None,created=False,**kwargs):
    if created:
        Customer.objects.create(user=instance)
        print("Customer has been created using decorator")

# class BearerAuthentication(TokenAuthentication):
#     """
#     Simple token based authentication.
#
#     Clients should authenticate by passing the token key in the 'Authorization'
#     HTTP header, prepended with the string 'Bearer '.  For example:
#
#     Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
#     """
#     keyword = 'Bearer'


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user.email)
        token, created = Token.objects.get_or_create(user=user)
        if created:
            context = {"result": "Here is your new token", "Token": token.key}
            return Response(context, status=status.HTTP_201_CREATED)
        context = {"result": "Logged in Successfully"}
        return Response(context, status=status.HTTP_200_OK)
