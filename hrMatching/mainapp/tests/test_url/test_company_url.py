from django.test import TestCase
from django.urls import resolve, reverse
from . import UrlTests
from ...models import User,Company
from ...views import company

class companysignupUrlTests(UrlTests, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "company_signup"
        cls.url = "accounts/signup/company"
        cls.template = "registration/company_signup_form.html"
        cls.view_class = company.CompanySignUpView
        cls.view_func = None
        cls.args = {}


class company_url_tests(UrlTests):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@email.com",
            password="123456"
            )
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name="test company name",
            city="Test City",
            phone="1234567890",
        )


class companyupdateUrlTests(company_url_tests, TestCase):

    def setUp(self):
        self.name = "company_update"
        self.view_class = company.CompanyUpdateView
        self.url = f"company/{self.company.pk}/update/0"
        self.template = "mainapp/company/company_update.html"
        self.args = {"pk": self.company.pk, "changed": 0}
        self.view_func = None
        self.client.login(email="test@email.com", password="123456")


class companydetailsUrlTests(company_url_tests, TestCase):

    def setUp(self):
        self.name = "company_detail"
        self.view_class = company.CompanyDetailView
        self.url = f"company/{self.company.pk}/details"
        self.template = "mainapp/company/company_detail.html"
        self.args = {"pk": self.company.pk}
        self.view_func = None
