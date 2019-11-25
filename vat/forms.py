from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *




class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email',)


class AmountForm(forms.ModelForm):
    class Meta:
        model = Amount
        fields = '__all__'


class ProductForm(forms.ModelForm):


    class Meta:
        model = Product
        fields = '__all__'


class ProductFormEdit(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'