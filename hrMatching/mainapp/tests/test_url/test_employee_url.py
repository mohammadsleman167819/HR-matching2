from django.test import TestCase
from django.urls import resolve, reverse
from . import UrlTests
from ...models import User,Employee
from ...views import employee
from .. import twenty_years_ago


class employeesignupUrlTests(UrlTests, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "employee_signup"
        cls.url = "accounts/signup/employee"
        cls.template = "registration/employee_signup_form.html"
        cls.view_class = employee.EmployeeSignUpView
        cls.view_func = None
        cls.args = {}


class employee_url_tests(UrlTests):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@email.com",
            password="123456"
            )
        cls.user.save()
        cls.employee = Employee.objects.create(
            user=cls.user,
            firstname="Mo",
            lastname="Soleman",
            dateOfBirth=twenty_years_ago,
            gender="MALE",
            city="Test City",
            phone="1234567890",
            skills="Python, Django",
        )
    
class employeeupdateUrlTests(employee_url_tests, TestCase):
    def setUp(self):
        self.name = "employee_update"
        self.view_class = employee.EmployeeUpdateView
        self.url = f"employee/{self.employee.pk}/update/0"
        self.template = "mainapp/employee/employee_update.html"
        self.args = {"pk": self.employee.pk, "changed": 0}
        self.view_func = None
        self.client.login(email="test@email.com", password="123456")

class employeedetailsUrlTests(employee_url_tests, TestCase):
    def setUp(self):
        self.name = "employee_detail"
        self.view_class = employee.EmployeeDetailView
        self.url = f"employee/{self.employee.pk}/details"
        self.template = "mainapp/employee/employee_detail.html"
        self.args = {"pk": self.employee.pk}
        self.view_func = None
