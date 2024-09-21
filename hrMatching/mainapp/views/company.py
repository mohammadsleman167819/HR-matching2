from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView,UpdateView
from django.urls import reverse

from ..forms.company import CompanySignUpForm,CompanyUpdateForm
from ..models import User,Company

class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'registration/company_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = 'mainapp/company_update.html'

    def get_success_url(self):
        return reverse('company_update', kwargs={'pk': self.object.pk , 'changed' : 1})


