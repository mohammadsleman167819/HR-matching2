from datetime import date, timedelta
from django.test import TestCase
from ..forms.company import CompanySignUpForm
from ..forms.employee import EmployeeSignUpForm
from ..models import Company, Employee, User
from . import company_data, employee_data


class CompanySignUpFormTest(TestCase):

    def test_form_valid_data(self):
        form = CompanySignUpForm(data=company_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        invalid_phone_company_data = company_data.copy()
        # Invalid phone number
        invalid_phone_company_data["phone"] = "123-456-789A"
        form = CompanySignUpForm(data=invalid_phone_company_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertEqual(
            form.errors["phone"],
            ["Phone number can only contain digits, hyphens, and plus signs."],
        )

    def test_form_save(self):
        form = CompanySignUpForm(data=company_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(Company.objects.filter(
                            user=user,
                            name="Test Company"
                            ).exists()
                        )


class EmployeeSignUpFormTest(TestCase):

    def test_form_valid_data(self):
        form = EmployeeSignUpForm(data=employee_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        invalid_phone_employee_data = employee_data.copy()
        invalid_phone_employee_data["phone"] = "123-456-789A"
        form = EmployeeSignUpForm(data=invalid_phone_employee_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertEqual(
            form.errors["phone"],
            ["Phone number can only contain digits, hyphens, and plus signs."],
        )

    def test_form_invalid_dateOfBirth_in_the_future(self):
        tomorrow = date.today() + timedelta(days=1)
        born_in_future_employee = employee_data.copy()
        born_in_future_employee["dateOfBirth"] = tomorrow
        form = EmployeeSignUpForm(data=born_in_future_employee)
        self.assertFalse(form.is_valid())
        self.assertIn("dateOfBirth", form.errors)
        self.assertEqual(
            form.errors["dateOfBirth"],
            ["Date of birth cannot be in the future."]
        )

    def test_form_invalid_dateOfBirth_younger_than_16(self):
        ten_years_ago = date.today().replace(year=date.today().year - 10)

        younger_than_16_employee = employee_data.copy()
        younger_than_16_employee["dateOfBirth"] = ten_years_ago
        form = EmployeeSignUpForm(
            data=younger_than_16_employee
        )
        self.assertFalse(form.is_valid())
        self.assertIn("dateOfBirth", form.errors)
        self.assertEqual(
            form.errors["dateOfBirth"],
            ["You must be at least 16 years old to register."],
        )

    def test_form_invalid_dateOfBirth_older_than_80(self):
        ninety_years_ago = date.today().replace(year=date.today().year - 90)
        older_than_80_employee = employee_data.copy()
        older_than_80_employee["dateOfBirth"] = (
            ninety_years_ago
        )
        form = EmployeeSignUpForm(data=older_than_80_employee)
        self.assertFalse(form.is_valid())
        self.assertIn("dateOfBirth", form.errors)
        self.assertEqual(
            form.errors["dateOfBirth"],
            ["Sorry you must be under 80."]
            )

    def test_form_save(self):
        form = EmployeeSignUpForm(data=employee_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        self.assertTrue(Employee.objects.filter(
                                user=user,
                                firstname="Mo"
                                ).exists())
