from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=30)
    producer = models.CharField(max_length=30)
    description = models.TextField(max_length=150)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media')


class Amount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , blank= True)
    amount = models.IntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    product_list = models.ManyToManyField(Amount, blank=True)


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product_list = models.ForeignKey(Cart, on_delete=models.CASCADE)
    enter_date = models.DateField()
    payment_deadline = models.DateField()
    summary_price = models.IntegerField()


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    home_number = models.CharField(max_length=30)
    local_number = models.CharField(max_length=30)
    post = models.CharField(max_length=30)
    city = models.CharField(max_length=30)



