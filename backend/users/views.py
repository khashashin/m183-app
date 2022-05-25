from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

from users.forms import LoginForm, SignupForm


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class RegisterView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')
