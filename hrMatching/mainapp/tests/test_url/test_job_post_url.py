from django.test import TestCase
from django.urls import resolve, reverse
from . import UrlTests
from ...models import Job_Post,User,Company
from ...views import job_post

class job_post_url_tests(UrlTests):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@email.com",
            password="123456",
            is_company=True
        )
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name="Company",
            city="Test City",
            phone="1234567890",
        )

        cls.post = Job_Post.objects.create(
            company = cls.company,
            job_title = "Backend",
            jobDescription = "Backend developer needed",
            workhours = "Full time",
            contact = "hr@mail.com",
            city = "Damascus",
            salary = "30K",
        )


class job_post_createUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.client.login(email="test@email.com", password="123456")
        self.name = "job_post_create"
        self.url = "job_post/create"
        self.template = "mainapp/job_post/job_post_create.html"
        self.view_class = job_post.Job_PostCreateView
        self.view_func = None
        self.args = {}
        self.client.login(email="test@email.com", password="123456")



class job_post_updateUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.name = "job_post_update"
        self.url = f"job_post/{self.post.job_id}/update/0"
        self.template = "mainapp/job_post/job_post_update.html"
        self.view_class = job_post.Job_PostUpdateView
        self.view_func = None
        self.args = {'pk' : self.post.job_id , 'changed' : 0}
        self.client.login(email="test@email.com", password="123456")


class job_post_detailsUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.name = "job_post_detail"
        self.url = f"job_post/{self.post.job_id}/details"
        self.template = "mainapp/job_post/job_post_detail.html"
        self.view_class = job_post.Job_PostDetailView
        self.view_func = None
        self.args = {'pk' : self.post.job_id}


class job_post_listUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.name = "job_post_list"
        self.url = "job_post/list"
        self.template = "mainapp/job_post/job_post_list.html"
        self.view_class = job_post.Job_PostListView
        self.view_func = None
        self.args = {}

class job_post_company_listUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.name = "job_post_company_list"
        self.url = "job_post/list/mine"
        self.template = "mainapp/job_post/job_post_list.html"
        self.view_class = job_post.Job_Post_Company_ListView
        self.view_func = None
        self.args = {}
        self.client.login(email="test@email.com", password="123456")

class job_post_deleteUrlTests(job_post_url_tests, TestCase):

    def setUp(self):
        self.name = "job_post_delete"
        self.url = f"job_post/{self.post.job_id}/delete"
        self.template = "mainapp/job_post/job_post_delete.html"
        self.view_class = job_post.Job_PostDeleteView
        self.view_func = None
        self.args = {'pk' : self.post.job_id}
        self.client.login(email="test@email.com", password="123456")