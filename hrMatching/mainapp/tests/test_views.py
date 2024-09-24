from django.test import TestCase
from ..views import home,company,employee
from ..models import Employee,User,Company
from datetime import date
from django.urls import reverse, resolve
import re
from . import *


class SignedinUserTests(object):
    
    url_name = None
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
    

    def test_redirected(self):
        self.client.login(email='test@email.com', password='123456')
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))    

 
class signupViewTests(SignedinUserTests,TestCase):
    def setUp(self):
        self.url_name = 'signup'

class loginViewTests(SignedinUserTests,TestCase):
    def setUp(self):
        self.url_name = 'login'


class EmployeeSignUpViewTests(SignedinUserTests,TestCase):
    def setUp(self):
        self.url_name = 'employee_signup'

class CompanySignUpViewTests(SignedinUserTests,TestCase):
    def setUp(self):
        self.url_name = 'company_signup'


class UpdateViewTests(object):
    
    def test_non_signed_in_cannot_view(self):
        response = self.client.get(reverse(self.url_name,kwargs=self.args))
        self.assertEqual(response.status_code,302)
        self.assertTrue(re.match(r'/accounts/login.*', response['Location']))
            
        
    def test_employee_not_owner_cannot_view(self):
        self.user2 = User.objects.create_user(email='test2@email.com', password='123456')
        self.user2.save()
        self.employee2 = Employee.objects.create(
            user=self.user2,
            firstname='Jo',
            lastname='Xien',
            dateOfBirth=twenty_years_ago,
            gender='MALE',
            city='Test City2',
            phone='12345678902',
            skills='c++,c#')
        self.client.login(email='test2@email.com', password='123456')
        response = self.client.get(reverse(self.url_name,kwargs=self.args))
        self.assertEqual(response.status_code,403)  
    
    def test_company_not_owner_cannot_view(self):
        self.user2 = User.objects.create_user(email='test2@email.com', password='123456')
        self.user2.save()
        self.company = Company.objects.create(
            user=self.user2,
            name = 'com',
            city='Test City2',
            phone='12345678902',
            )
        self.client.login(email='test2@email.com', password='123456')
        response = self.client.get(reverse(self.url_name,kwargs=self.args))
        self.assertEqual(response.status_code,403)
    
    def test_owner_can_view(self):
        self.client.login(email='test@email.com', password='123456')
        response = self.client.get(reverse(self.url_name,kwargs=self.args))
        self.assertEqual(response.status_code,200)

class EmployeeUpdateViewTests(TestCase,UpdateViewTests):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.employee = Employee.objects.create(
            user=cls.user,
            firstname='Mo',
            lastname='Soleman',
            dateOfBirth=twenty_years_ago,
            gender='MALE',
            city='Test City',
            phone='1234567890',
            skills='Python, Django')
        cls.url_name = 'employee_update'
        cls.args = {'pk': cls.employee.pk ,'changed': 0}
    
    
    def test_doing_an_update(self):
        self.client.login(email='test@email.com', password='123456')
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(url, {
            'firstname': 'Mohammad',
            'lastname': 'Soleman',
            'dateOfBirth': twenty_years_ago,
            'gender':'MALE',
            'city':'Test City',
            'phone':'1234567890',
            'skills':'Python, Django'
        })
        self.assertRedirects(response, reverse(self.url_name, kwargs={'pk': self.employee.pk, 'changed': 1}))
        
        # Refresh the employee instance from the database
        self.employee.refresh_from_db()

        # Check if the employee instance has been updated
        self.assertEqual(self.employee.firstname, 'Mohammad')

class CompanyUpdateViewTests(TestCase,UpdateViewTests):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name='Co12',
            city='Test City',
            phone='1234567890',
            )
        cls.url_name = 'company_update'
        cls.args = {'pk': cls.company.pk ,'changed': 0}
    
    
    def test_doing_an_update(self):
        self.client.login(email='test@email.com', password='123456')
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(url, {
            'name':'Company Name',
            'city':'Test City',
            'phone':'1234567890',
        })
        self.assertRedirects(response, reverse(self.url_name, kwargs={'pk': self.company.pk, 'changed': 1}))
        
        # Refresh the company instance from the database
        self.company.refresh_from_db()

        # Check if the company instance has been updated
        self.assertEqual(self.company.name, 'Company Name')


