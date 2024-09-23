"""from django.test import TestCase
from django import forms
from ..forms.company import CompanySignUpForm,CompanyUpdateForm
from ..forms.employee import EmployeeSignUpForm

from ..models import Company,User,Employee
from datetime import date


    
class CompanySignUpFormTest(TestCase):

    def test_form_valid_data(self):
        form = CompanySignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'name': 'Test Company',
            'city': 'Test City',
            'phone': '123-456-7890'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        form = CompanySignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'name': 'Test Company',
            'city': 'Test City',
            'phone': '123-456-789A'  # Invalid phone number
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'], ['Phone number can only contain digits, hyphens, and plus signs.'])

    
    def test_form_save(self):
        form = CompanySignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'name': 'Test Company',
            'city': 'Test City',
            'phone': '123-456-7890'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(Company.objects.filter(user=user, name='Test Company').exists())


class EmployeeSignUpFormTest(TestCase):

    def test_form_valid_data(self):
        form = EmployeeSignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'firstname': 'Mo',
            'lastname': 'Soleman',
            'dateOfBirth': date(2001, 1, 1),
            'gender': 'MALE',        
            'city': 'Test City',     
            'phone': '1234567890',   
            'education': '',   
            'experience': '',   
            'awards': '',  
            'hobbies': '', 
            'skills': 'Python, Django',
            'references': '',
            'other': ''
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        form = EmployeeSignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'name': 'Test Company',
            'city': 'Test City',
            'phone': '123-456-789A'  # Invalid phone number
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'], ['Phone number can only contain digits, hyphens, and plus signs.'])

    
    def test_form_save(self):
        form = EmployeeSignUpForm(data={
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'firstname': 'Mo',
            'lastname': 'Soleman',
            'dateOfBirth': date(2001, 1, 1),
            'gender': 'MALE',        
            'city': 'Test City',     
            'phone': '1234567890',   
            'education': '',   
            'experience': '',   
            'awards': '',  
            'hobbies': '', 
            'skills': 'Python, Django',
            'references': '',
            'other': ''
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(Employee.objects.filter(user=user, firstname='Mo').exists())
"""