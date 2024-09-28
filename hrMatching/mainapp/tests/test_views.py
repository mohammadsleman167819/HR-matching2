import re
from django.test import TestCase
from django.urls import reverse
from ..models import Company, Employee, User, Job_Post
from . import twenty_years_ago


class SignedinUserRestrictionsTests(object):
    """ Test that a signed in user can't view the url in url_name"""
    url_name = None
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@email.com",
            password="123456"
            )
        cls.user.save()

    def test_redirected(self):
        self.client.login(email="test@email.com", password="123456")
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))


class signupViewTests(SignedinUserRestrictionsTests, TestCase):
    def setUp(self):
        self.url_name = "signup"


class loginViewTests(SignedinUserRestrictionsTests, TestCase):
    def setUp(self):
        self.url_name = "login"


class EmployeeSignUpViewTests(SignedinUserRestrictionsTests, TestCase):
    def setUp(self):
        self.url_name = "employee_signup"


class CompanySignUpViewTests(SignedinUserRestrictionsTests, TestCase):
    def setUp(self):
        self.url_name = "company_signup"


class OnlySignedOwnerTests(object):

    def test_non_signed_in_cannot_view(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.args))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(re.match(r"/accounts/login.*", response["Location"]))

    def test_employee_not_owner_cannot_view(self):
        self.user2 = User.objects.create_user(
            email="test2@email.com", password="123456",is_employee=True
        )
        self.user2.save()
        self.employee2 = Employee.objects.create(
            user=self.user2,
            firstname="Jo",
            lastname="Xien",
            dateOfBirth=twenty_years_ago,
            gender="MALE",
            city="Test City2",
            phone="12345678902",
            skills="c++,c#",
        )
        self.client.login(email="test2@email.com", password="123456")
        response = self.client.get(reverse(self.url_name, kwargs=self.args))
        self.assertEqual(response.status_code, 403)

    def test_company_not_owner_cannot_view(self):
        self.user2 = User.objects.create_user(
            email="test2@email.com", password="123456",is_company=True
        )
        self.user2.save()
        self.company = Company.objects.create(
            user=self.user2,
            name="com",
            city="Test City2",
            phone="12345678902",
        )
        self.client.login(email="test2@email.com", password="123456")
        response = self.client.get(reverse(self.url_name, kwargs=self.args))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view(self):
        self.client.login(email="test@email.com", password="123456")
        response = self.client.get(reverse(self.url_name, kwargs=self.args))
        self.assertEqual(response.status_code, 200)


class EmployeeUpdateViewTests(TestCase, OnlySignedOwnerTests):

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
        cls.url_name = "employee_update"
        cls.args = {"pk": cls.employee.pk, "changed": 0}

    def test_doing_an_update(self):
        self.client.login(email="test@email.com", password="123456")
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(
            url,
            {
                "firstname": "Mohammad",
                "lastname": "Soleman",
                "dateOfBirth": twenty_years_ago,
                "gender": "MALE",
                "city": "Test City",
                "phone": "1234567890",
                "skills": "Python, Django",
            },
        )
        self.assertRedirects(
            response,
            reverse(self.url_name,
                    kwargs={"pk": self.employee.pk, "changed": 1}
                    )
        )

        # Refresh the employee instance from the database
        self.employee.refresh_from_db()

        # Check if the employee instance has been updated
        self.assertEqual(self.employee.firstname, "Mohammad")


class CompanyUpdateViewTests(TestCase, OnlySignedOwnerTests):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="test@email.com",
            password="123456"
            )
        cls.user.save()
        cls.company = Company.objects.create(
            user=cls.user,
            name="Co12",
            city="Test City",
            phone="1234567890",
        )
        cls.url_name = "company_update"
        cls.args = {"pk": cls.company.pk, "changed": 0}

    def test_doing_an_update(self):
        self.client.login(email="test@email.com", password="123456")
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(
            url,
            {
                "name": "Company Name",
                "city": "Test City",
                "phone": "1234567890",
            },
        )
        self.assertRedirects(
            response,
            reverse(self.url_name,
                    kwargs={"pk": self.company.pk, "changed": 1}
                    )
        )

        # Refresh the company instance from the database
        self.company.refresh_from_db()

        # Check if the company instance has been updated
        self.assertEqual(self.company.name, "Company Name")


class Job_PostCreateViewTests(TestCase):

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
            name="Co12",
            city="Test City",
            phone="1234567890",
        )

        cls.url_name = "job_post_create"
        cls.args = {}

    def test_creating_job_post(self):
        self.client.login(email="test@email.com", password="123456")
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(
            url,
            {
                'job_title' : 'Created Backend',
                'jobDescription' : 'Backend developer needed',
                'workhours' : 'Full time',
                'contact' : 'hr@mail.com',
                'city' : 'Damascus',
                'salary' : '30K',
             },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
                Job_Post.objects.filter(
                    job_id=1,
                    job_title='Created Backend'
                ).exists()
            )
        self.job_post = Job_Post.objects.get(
                    job_id=1,
                    job_title='Created Backend'
                )

        self.assertRedirects(
            response,
            reverse("job_post_detail",
                    kwargs={"pk": self.job_post.job_id}
                    )
        )

        self.assertEqual(self.job_post.company, self.company)

    def test_non_signed_in_cannot_view(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.args))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(re.match(r"/accounts/login.*", response["Location"]))




class Job_PostUpdateViewTests(TestCase, OnlySignedOwnerTests):

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
            name="Co12",
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

        cls.url_name = "job_post_update"
        cls.args = {"pk": cls.post.job_id, "changed": 0}

    def test_doing_an_update(self):
        self.client.login(email="test@email.com", password="123456")
        url = reverse(self.url_name, kwargs=self.args)
        response = self.client.post(
            url,
            {
                'job_title' : 'Frontend',
                'jobDescription' : 'Backend developer needed',
                'workhours' : 'Full time',
                'contact' : 'hr@mail.com',
                'city' : 'Damascus',
                'salary' : '30K',
             },
        )
        self.assertRedirects(
            response,
            reverse(self.url_name,
                    kwargs={"pk": self.post.job_id, "changed": 1}
                    )
        )

        # Refresh the job_post instance from the database
        self.post.refresh_from_db()

        # Check if the job_post instance has been updated
        self.assertEqual(self.post.job_title, "Frontend")





class Job_PostListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            email="test1@email.com",
            password="123456",
            is_company=True
            )
        cls.user1.save()
        cls.company1 = Company.objects.create(
            user=cls.user1,
            name="Co1",
            city="Test City",
            phone="1234567890",
        )

        cls.user2 = User.objects.create_user(
            email="test2@email.com",
            password="123456",
            is_company=True
            )
        cls.user2.save()
        cls.company2 = Company.objects.create(
            user=cls.user2,
            name="Co2",
            city="Test City",
            phone="1234567890",
        )

        # 10 for each company
        for num in range(20):
            company = cls.company1
            if num%2==0:
                company = cls.company2

            Job_Post.objects.create(
            company = company,
            job_title = f"title{num}",
            jobDescription = f"des{num}",
            workhours = f"hours{num}",
            contact = f"hr{num}@mail.com",
            city = f"city{num}",
            salary = "30K",
            )

    def setUp(self):
        self.url_name = 'job_post_list'

    def test_pagination_is_nine(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['Job_Post_list']), 9)

    def test_lists_all_posts(self):
        # Get third page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse(self.url_name)+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['Job_Post_list']), 2)

class Job_Post_Company_ListViewTests(Job_PostListViewTests):

    def setUp(self):
        self.url_name = 'job_post_company_list'
        self.client.login(email="test1@email.com", password="123456")

    def test_lists_all_posts(self):
        # Get second page and confirm it has (exactly) remaining 1 items
        self.client.login(email="test1@email.com", password="123456")
        response = self.client.get(reverse(self.url_name)+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['Job_Post_list']), 1)

    def test_shows_only_for_signed_in_company(self):
        self.user3 = User.objects.create_user(
            email="test3@email.com",
            password="123456",
            is_company=True
            )
        self.company3 = Company.objects.create(
            user=self.user3,
            name="Co3",
            city="Test City",
            phone="1234567890",
        )

        #add no posts by company
        self.client.login(email="test3@email.com", password="123456")
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['Job_Post_list']), 0)

