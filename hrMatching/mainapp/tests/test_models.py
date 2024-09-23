"""from django.test import TestCase
from ..models import Employee,User,Company
from datetime import date

class EmployeeModelTest(TestCase):
    def setUp(self):
        # Create a User instance
        self.user = User.objects.create(email='test@email.com', password='123456')
        # Create an Employee instance
        self.employee = Employee.objects.create(
            user=self.user,
            firstname='Mo',
            lastname='Soleman',
            dateOfBirth=date(2001, 1, 1),
            gender='MALE',
            city='Test City',
            phone='1234567890',
            skills='Python, Django'
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), 'Mo Soleman')

    def test_get_absolute_url(self):
        self.assertEqual(self.employee.get_absolute_url(),f'/employee/{self.employee.pk}/details')

    def test_get_fields(self):
        fields = self.employee.get_fields()
        expected_fields = [
            ('First Name', 'Mo'),
            ('Last Name', 'Soleman'),
            ('Age', self.employee.get_age()),
            ('Gender', 'MALE'),
            ('City', 'Test City'),
            ('Phone', '1234567890'),
            ('Education', ''),
            ('Experience', ''),
            ('Awards', ''),
            ('Hobbies', ''),
            ('Skills', 'Python, Django'),
            ('References', ''),
            ('Other', '')
            
        ]
        self.assertEqual(fields, expected_fields)


class CompanyModelTest(TestCase):
    def setUp(self):
        # Create a User instance
        self.user = User.objects.create(email='test@email.com', password='123456')
        # Create an Company instance
        self.company = Company.objects.create(
            user=self.user,
            name='Company',
            city='Test City',
            phone='1234567890',
        )

    def test_company_str(self):
        self.assertEqual(str(self.company), 'Company')

    def test_get_absolute_url(self):
        self.assertEqual(self.company.get_absolute_url(),f'/company/{self.company.pk}/details' )

    def test_get_fields(self):
        fields = self.company.get_fields()
        expected_fields = [
            ('Name', 'Company'),
            ('City', 'Test City'),
            ('Phone', '1234567890'),
        ]
        self.assertEqual(fields, expected_fields)
"""