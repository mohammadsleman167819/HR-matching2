from ..forms.employee import EmployeeSignUpForm, EmployeeUpdateForm
from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..models import User, Employee
from django.contrib.auth import login


class EmployeeSignUpView(UserPassesTestMixin, CreateView):
    """
    View to handle sign-up for employee user type

    - add user_type = emplpoyee to cotext
    - redirect to home page after logging in
    - deny permission for already authenticated users and redirect them to home
    """

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


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update employee user type information

    - redirect with Get[changed] set to 1 after sucessfully updateing
    - deny permission for any one but account owner
    """

    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'mainapp/employee/employee_update.html'

    def get_success_url(self):
        return reverse(
            'employee_update',
            kwargs={
                'pk': self.object.pk,
                'changed': 1
            }
        )

    def test_func(self):
        return self.get_object().user.id == self.request.user.id


class EmployeeDetailView(DetailView):
    """view to list employee details """
    model = Employee
    template_name = "mainapp/employee/employee_detail.html"
