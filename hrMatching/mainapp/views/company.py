from ..forms.company import CompanySignUpForm,CompanyUpdateForm
from . import *
class CompanySignUpView(UserPassesTestMixin,CreateView):
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
    
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')


class CompanyUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = 'mainapp/company/company_update.html'

    def get_success_url(self):
        return reverse('company_update', kwargs={'pk': self.object.pk , 'changed' : 1})

    def test_func(self):
        return self.get_object().user.id == self.request.user.id


class CompanyDetailView(DetailView):
    model = Company
    template_name = "mainapp/company/company_detail.html"

