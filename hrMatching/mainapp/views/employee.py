from django.contrib.auth import login
from django.shortcuts import redirect,reverse
from django.views.generic import CreateView,UpdateView

from ..forms.employee import EmployeeSignUpForm,EmployeeUpdateForm
from ..models import User,Employee

class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'registration/employee_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'mainapp/employee_update.html'

    def get_success_url(self):
        return reverse('employee_update' , kwargs={ 'pk': self.object.pk ,'changed': 1})
