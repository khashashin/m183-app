from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']