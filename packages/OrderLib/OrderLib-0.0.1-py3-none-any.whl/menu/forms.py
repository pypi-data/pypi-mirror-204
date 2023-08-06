from django import forms
from .models import Cupcake, Newcake
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

class CupcakeForm(forms.ModelForm):

    class Meta:
        model = Cupcake
        fields = ('name','rating','price','image','weight')
        
class NewcakeForm(forms.ModelForm):

    class Meta:
        model = Newcake
        fields = ('name','price','image','weight')
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validators.validate_email])
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'remember-me'}))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid username or password')
        return cleaned_data