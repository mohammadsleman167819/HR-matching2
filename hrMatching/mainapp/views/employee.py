from ..forms.employee import EmployeeSignUpForm,EmployeeUpdateForm
from . import *

class EmployeeSignUpView(UserPassesTestMixin,CreateView):
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
    
    
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')  


class EmployeeUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'mainapp/employee/employee_update.html'

    def get_success_url(self):
        return reverse('employee_update' , kwargs={ 'pk': self.object.pk ,'changed': 1})

    def test_func(self):
        return self.get_object().user.id == self.request.user.id




class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "mainapp/employee/employee_detail.html"
