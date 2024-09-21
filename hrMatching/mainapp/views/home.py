from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from ..forms.home import CustomLoginForm

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class LoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'



def index(request):
    return render(request, 'mainapp/index.html')