from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from datetime import date
from django.urls import reverse


class User(AbstractUser):
    """
    extend AbstractUser and do configurations

     - Create a new class called User that subclasses AbstractUser
     - Removed the username field
     - Made the email field required and unique
     - Set email as the unique identifier for the User model
     - Specified that all objects for the class come from the CustomUserManager
     - added flags to show the user type (employee/company)

    """

    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email_address", unique=True)
    is_employee = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Employee(models.Model):
    """
    Employee model handle users of type employee

    Has the following attributes:
        user : OneToOneField with User instance , primary key
        firstname, lastname, dateOfBirth, gender, city, phone,
        education, experience, awards, hobbies, skills, references, other
        cluster : IntegerField to store the cluster's number employee belong to
        clusterable_text : TextField contain text-preprocessed employee's info

    methods:
        __str__ : return firstname + lastname to represent inctanse
        get_age : calculate the employee age based on dateofbirth
        get_absolute_url : return url link to employee detail page
        get_fields : return fields we want to show in employee detail page
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(
        "First Name", max_length=100, help_text="Employee First Name"
    )
    lastname = models.CharField(
        "Last Name", max_length=100, help_text="Employee Last Name"
    )
    dateOfBirth = models.DateField("Date Of Birth", help_text="Employee Date of Birth")
    gender = models.CharField(
        "Gender", max_length=8, choices=[("MALE", "MALE"), ("FEMALE", "FEMALE")]
    )
    city = models.CharField("City", max_length=50, help_text="Employee City")
    phone = models.CharField("Phone", max_length=20, help_text="Employee Phone")
    education = models.TextField("Education", max_length=1000, null=True, blank=True)
    experience = models.TextField("Experience", max_length=1000, null=True, blank=True)
    awards = models.TextField("Awards", max_length=1000, null=True, blank=True)
    hobbies = models.TextField("Hobbies", max_length=1000, null=True, blank=True)
    skills = models.TextField("Skills", max_length=1000)
    references = models.TextField("References", max_length=1000, null=True, blank=True)
    other = models.TextField("Other", max_length=1000, null=True, blank=True)
    cluster = models.IntegerField("Cluster", null=True, blank=True)
    clusterable_text = models.TextField("Clusterable Text", null=True, blank=True)

    def __str__(self):
        """String for representing the Employee object (in Admin site etc.)."""
        return self.firstname + " " + self.lastname

    def get_age(self):
        """function return employee age based on thier birthday"""
        today = date.today()
        birthyear = self.dateOfBirth.year
        age = today.year - birthyear
        # Account for birthdays not yet passed in the current year
        my_birth_month = self.dateOfBirth.month
        my_birth_day = self.dateOfBirth.day
        if (today.month, today.day) < (my_birth_month, my_birth_day):
            age -= 1
        return str(age)

    def get_absolute_url(self):
        """Return url to page shows employee details"""
        return reverse("employee_detail", kwargs={"pk": self.pk})

    def get_fields(self):
        """return info to be showed in employee details page"""
        fields = []
        for field in self._meta.fields:
            if field.verbose_name not in [
                "user",
                "Clusterable Text",
                "Cluster",
                "Date Of Birth",
            ]:
                val = field.value_from_object(self)
                if val is None:
                    val = ""
                info = (field.verbose_name, val)
                fields.append(info)
            if field.verbose_name in ["Date Of Birth"]:
                info = ("Age", self.get_age())
                fields.append(info)
        return fields


class Company(models.Model):
    """
    Company model handle users of type company

    Has the following attributes:
        user : OneToOneField with User instance , primary key
        Contact information stored in CharFields (required):
            (name , city , phone)

    methods:
        __str__ : return name to represent inctanse
        get_absolute_url : return url link to company detail page
        get_fields : returns key-value pairs for use on company's detail page.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField("Name", max_length=100, help_text="Company Name")
    city = models.CharField("City", max_length=100, help_text="Company City")
    phone = models.CharField("Phone", max_length=20, help_text="Company Phone")

    def __str__(self):
        """String for representing the Company object (in Admin site etc.)."""
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def get_absolute_url(self):
        """Return url to page shows employee details"""
        return reverse("company_detail", kwargs={"pk": self.pk})

    def get_fields(self):
        """return fields (name,value) we want to show in company detail page"""
        return [
            (field.verbose_name, field.value_from_object(self))
            for field in self._meta.fields
            if field.verbose_name not in ["user"]
        ]


class Job_Post(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    job_title = models.CharField("Job Title", max_length=350)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobDescription = models.TextField("Job Description", max_length=5000)
    workhours = models.TextField("Work Hours", max_length=1000)
    contact = models.CharField("Contact", max_length=50)
    city = models.CharField("City", max_length=50)
    salary = models.CharField("Salary", max_length=50)
    cluster = models.IntegerField("Cluster", null=True, blank=True)
    added_date = models.DateField("Added on", auto_now_add=True)
    clusterable_text = models.TextField("Clusterable Text", null=True, blank=True)

    class Meta:
        verbose_name = "Job Post"
        ordering = ["-job_id"]

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Job_Post."""
        return reverse("job_post_detail", kwargs={"pk": self.job_id})

    def __str__(self):
        """String for representing the Job_POst object (in Admin site etc.)."""
        return self.job_title + " by " + self.company.name

    def get_fields(self):
        """return fields (name,value) we want to show in Job Post detail page"""
        fields = []
        for field in self._meta.fields:
            if field.verbose_name not in [
                "job id",
                "company",
                "Clusterable Text",
                "Cluster",
            ]:
                val = field.value_from_object(self)
                if val is None:
                    val = ""
                info = (field.verbose_name, val)
                fields.append(info)
            if field.verbose_name in ["company"]:
                company = field.value_from_object(self)
                company_obj = Company.objects.get(user=company)
                info = ("Company", company_obj)
                fields.append(info)
        return fields
