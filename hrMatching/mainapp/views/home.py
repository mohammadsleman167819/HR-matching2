from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from ..forms.home import CustomLoginForm
from . import *
 
class SignUpView(UserPassesTestMixin,TemplateView):
    template_name = 'registration/signup.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')

class LoginView(UserPassesTestMixin,LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')



def index(request):
    return render(request, 'mainapp/index.html')


def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)