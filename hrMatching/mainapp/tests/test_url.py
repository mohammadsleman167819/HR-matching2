from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home,company,employee
from ..models import Employee,User,Company
from datetime import date

class UrlTests(object):
    
    def test_url_status_code(self):
        url = reverse(self.name,kwargs = self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_view(self):
        url = reverse(self.name,kwargs = self.args)
        resolved_view = resolve(url).func
        
        if self.view_class:
            self.assertEqual(resolved_view.view_class, self.view_class)
        elif self.view_func:
            self.assertEqual(resolved_view.__name__, self.view_func.__name__)  # Compare function names
            self.assertEqual(resolved_view.__module__, self.view_func.__module__)  # Optionally compare the module

    def test_url_uses_correct_template(self):
        url = reverse(self.name,kwargs = self.args)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)

    def test_url_reverse(self):
        url = reverse(self.name,kwargs = self.args)
        self.assertEqual(url, '/' + self.url)


class SignUpUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'signup'
        cls.url = 'accounts/signup/'
        cls.template = 'registration/signup.html'
        cls.view_class = home.SignUpView
        cls.view_func = None
        cls.args = {}



class indexUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'index'
        cls.url = ''
        cls.template = 'mainapp/index.html'
        cls.view_func = home.index
        cls.view_class = None
        cls.args = {}




class employeesignupUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'employee_signup'
        cls.url = 'accounts/signup/employee'
        cls.template = 'registration/employee_signup_form.html'
        cls.view_class = employee.EmployeeSignUpView
        cls.view_func = None
        cls.args = {}


class companysignupUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'company_signup'
        cls.url = 'accounts/signup/company'
        cls.template = 'registration/company_signup_form.html'
        cls.view_class = company.CompanySignUpView
        cls.view_func = None
        cls.args = {}


class loginUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'login'
        cls.url = 'accounts/login'
        cls.template = 'registration/login.html'
        cls.view_class = home.LoginView
        cls.view_func = None
        cls.args = {}


class employeeupdateUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.employee = Employee.objects.create(
            user=cls.user,
            firstname='Mo',
            lastname='Soleman',
            dateOfBirth=date(2001, 1, 1),
            gender='MALE',
            city='Test City',
            phone='1234567890',
            skills='Python, Django'
        )
        cls.name = 'employee_update'
        cls.view_class = employee.EmployeeUpdateView
        cls.url = f'employee/{cls.employee.pk}/update/0'
        cls.template = 'mainapp/employee/employee_update.html'  
        cls.args={ 'pk': cls.employee.pk ,'changed': 0}
        cls.view_func = None
        
    def setUp(self):
        self.client.login(email='test@email.com', password='123456')
  
class companyupdateUrlTests(UrlTests,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name = 'test company name',
            city='Test City',
            phone='1234567890'
        )
        cls.name = 'company_update'
        cls.view_class = company.CompanyUpdateView
        cls.url = f'company/{cls.company.pk}/update/0'
        cls.template = 'mainapp/company/company_update.html'  
        cls.args={ 'pk': cls.company.pk ,'changed': 0}
        cls.view_func = None
        
        
    def setUp(self):
        self.client.login(email='test@email.com', password='123456')
    

class employeedetailsUrlTests(UrlTests,TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.employee = Employee.objects.create(
            user=cls.user,
            firstname='Mo',
            lastname='Soleman',
            dateOfBirth=date(2001, 1, 1),
            gender='MALE',
            city='Test City',
            phone='1234567890',
            skills='Python, Django'
        )
        cls.name = 'employee_detail'
        cls.view_class = employee.EmployeeDetailView
        cls.url = f'employee/{cls.employee.pk}/details'
        cls.template = 'mainapp/employee/employee_detail.html'  
        cls.args={ 'pk': cls.employee.pk}
        cls.view_func = None
        
class companydetailsUrlTests(UrlTests,TestCase): 
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name = 'test company name',
            city='Test City',
            phone='1234567890'
        )
        cls.name = 'company_detail'
        cls.view_class = company.CompanyDetailView
        cls.url = f'company/{cls.company.pk}/details'
        cls.template = 'mainapp/company/company_detail.html'  
        cls.args={ 'pk': cls.company.pk}
        cls.view_func = None
