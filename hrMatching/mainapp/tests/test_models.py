from django.test import TestCase
from ..models import Employee,User,Company
from datetime import date
#valid value for employee Date of Birth
twenty_years_ago = date.today().replace(year=date.today().year - 20)


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.employee = Employee.objects.create(
            user=cls.user,
            firstname='Mo',
            lastname='Soleman',
            dateOfBirth=twenty_years_ago,
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
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@email.com', password='123456')
        cls.company = Company.objects.create(
            user=cls.user,
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
