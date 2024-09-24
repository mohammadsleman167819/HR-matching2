from django.test import TestCase
from django import forms
from ..forms.company import CompanySignUpForm,CompanyUpdateForm
from ..forms.employee import EmployeeSignUpForm,EmployeeUpdateForm
from ..models import Company,User,Employee
from datetime import date, timedelta
from . import *

class CompanySignUpFormTest(TestCase):

    def test_form_valid_data(self):
        form = CompanySignUpForm(data=company_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        invalid_phone_company_data = company_data.copy()
        invalid_phone_company_data['phone'] = '123-456-789A'  # Invalid phone number
        form = CompanySignUpForm(data=invalid_phone_company_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'], ['Phone number can only contain digits, hyphens, and plus signs.'])

    
    def test_form_save(self):
        form = CompanySignUpForm(data=company_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(Company.objects.filter(user=user, name='Test Company').exists())





class EmployeeSignUpFormTest(TestCase):
    

    def test_form_valid_data(self):
        form = EmployeeSignUpForm(data=employee_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        invalid_phone_employee_data = employee_data.copy()
        invalid_phone_employee_data['phone'] = '123-456-789A'
        form = EmployeeSignUpForm(data=invalid_phone_employee_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'], ['Phone number can only contain digits, hyphens, and plus signs.'])

    def test_form_invalid_dateOfBirth_in_the_future(self):
        tomorrow = date.today() + timedelta(days=1)
        invaled_dateOfBirth_in_future_employee_data = employee_data.copy()
        invaled_dateOfBirth_in_future_employee_data['dateOfBirth'] = tomorrow
        form = EmployeeSignUpForm(data=invaled_dateOfBirth_in_future_employee_data)
        self.assertFalse(form.is_valid())
        self.assertIn('dateOfBirth', form.errors)
        self.assertEqual(form.errors['dateOfBirth'], ['Date of birth cannot be in the future.'])

    def test_form_invalid_dateOfBirth_younger_than_16(self):
        ten_years_ago = date.today().replace(year=date.today().year - 10)
        
        invaled_dateOfBirth_younger_than_16_employee_data = employee_data.copy()
        invaled_dateOfBirth_younger_than_16_employee_data['dateOfBirth'] = ten_years_ago
        form = EmployeeSignUpForm(data=invaled_dateOfBirth_younger_than_16_employee_data)
        self.assertFalse(form.is_valid())
        self.assertIn('dateOfBirth', form.errors)
        self.assertEqual(form.errors['dateOfBirth'], ['You must be at least 16 years old to register.'])


    def test_form_invalid_dateOfBirth_older_than_80(self):
        ninety_years_ago = date.today().replace(year=date.today().year - 90)
        invaled_dateOfBirth_older_than_80_employee_data = employee_data.copy()
        invaled_dateOfBirth_older_than_80_employee_data['dateOfBirth'] = ninety_years_ago
        form = EmployeeSignUpForm(data=invaled_dateOfBirth_older_than_80_employee_data)
        self.assertFalse(form.is_valid())
        self.assertIn('dateOfBirth', form.errors)
        self.assertEqual(form.errors['dateOfBirth'], ['Sorry you must be under 80.'])

    def test_form_save(self):
        form = EmployeeSignUpForm(data=employee_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(Employee.objects.filter(user=user, firstname='Mo').exists())
