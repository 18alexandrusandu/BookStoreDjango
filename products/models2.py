from django.db import models

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user);
        token["id"]=user.id_user;
        token["firstName"]=user.first_name;
        token["lastName"]=user.last_name;
        token["userName"]=user.user_name;
        token["email"]=user.email;
        token["address"]=user.address;
        token["phone"]=user.phone;
        token["cardNumber"]=user.card_number;
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer;



class Orders(models.Model):
    id_order = models.BigAutoField( primary_key=True)
    date_time = models.DateTimeField()
    price = models.FloatField()
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'orders'



class Products(models.Model):
    id_product = models.BigAutoField(primary_key=True)
    author = models.CharField(max_length=60)
    category = models.CharField(max_length=40)
    description = models.TextField()
    image = models.TextField()
    price = models.FloatField()
    product_name = models.CharField(max_length=100)
    publishing_house = models.CharField(max_length=40)
    year = models.IntegerField()
    in_store = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'
# Create your models here.


class ProductsOrder(models.Model):
    id_product_order = models.BigAutoField(primary_key=True)
    amount = models.IntegerField()
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)

    class Meta:
       # managed = False
        db_table = 'products_order'


class Roles(models.Model):
    id_role = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
      #  managed = False
        db_table = 'roles'


class UserRole(models.Model):
    id_user_role = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'user_role'


class Users(models.Model):
    id_user = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    user_name = models.CharField(max_length=100)

    class Meta:
       # managed = False
        db_table = 'users'
