from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
class NewsLetterForm(forms.Form):
    username = forms.CharField(label='First_Name', max_length=30)
    email = forms.EmailField(label='Email Address')
    password = forms.PasswordInput()
    
    
class RegisterForm(UserCreationForm):
     email = forms.EmailField()
     
     class Meta:
         model = User
         fields = ['username', 'email', 'password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label= 'Username' , max_length=254)
    password = forms.CharField(label= 'Password', widget=forms.PasswordInput)
    
         
     
    