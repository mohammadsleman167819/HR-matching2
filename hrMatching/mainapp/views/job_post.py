from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from ..models import Job_Post,Company
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms.job_post import Job_PostUpdateForm, Job_PostCreateForm
from django.shortcuts import reverse
from django.urls import reverse_lazy

class Job_PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to create a Job_Post"""
    model = Job_Post
    form_class = Job_PostCreateForm
    template_name = "mainapp/job_post/job_post_create.html"

    def form_valid(self, form):
        form.instance.company = Company.objects.get(user = self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_company



class Job_PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update Job Post information

    - redirect with Get[changed] set to 1 after sucessfully updateing
    - deny permission for any one but Job Post owner
    """
    model = Job_Post
    form_class = Job_PostUpdateForm
    template_name = 'mainapp/job_post/job_post_update.html'

    def get_success_url(self):
        return reverse(
            'job_post_update',
            kwargs={
                'pk': self.object.job_id,
                'changed': 1
            }
        )

    def test_func(self):
        return self.get_object().company.user.id == self.request.user.id


class Job_PostDetailView(DetailView):
    """view to list company details """
    model = Job_Post
    template_name = "mainapp/job_post/job_post_detail.html"


class Job_PostListView(ListView):
    """view to list Job Posts"""
    model = Job_Post
    context_object_name = 'Job_Post_list'
    template_name = "mainapp/job_post/job_post_list.html"
    paginate_by = 9


class Job_Post_Company_ListView(LoginRequiredMixin, UserPassesTestMixin, Job_PostListView):
    """view to list Job Posts for one company"""
    def get_queryset(self):
        company = Company.objects.get(user=self.request.user)
        return Job_Post.objects.filter(company = company)

    def test_func(self):
        return self.request.user.is_company


class Job_PostDeleteView(DeleteView,LoginRequiredMixin, UserPassesTestMixin,):
    model = Job_Post
    template_name = "mainapp/job_post/job_post_delete.html"
    success_url = reverse_lazy('job_post_company_list')

    def test_func(self):
        user_is_company = self.request.user.is_company
        user_own_post = self.get_object().company.user.id == self.request.user.id
        return user_is_company and user_own_post

