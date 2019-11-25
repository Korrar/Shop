from django.contrib import admin
from django.apps import apps

from .models import *

Models = (Product, Order, UserAddress, Amount, Cart)

admin.site.register(Models)