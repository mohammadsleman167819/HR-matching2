from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from datetime import date
from django.urls import reverse


class User(AbstractUser):
    """
    extend AbstractUser and do configurations
    
     - Create a new class called User that subclasses AbstractUser
     - Removed the username field
     - Made the email field required and unique
     - Set the USERNAME_FIELD -- which defines the unique identifier for the User model -- to email
     - Specified that all objects for the class come from the CustomUserManager
    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email_address",unique=True)    
    is_employee = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()



class Employee(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname   = models.CharField("First Name",max_length=100, help_text='Employee First Name')
    lastname    = models.CharField("Last Name",max_length=100, help_text='Employee Last Name')
    dateOfBirth = models.DateField("Date Of Birth",help_text='Employee Date of Birth')
    gender      = models.CharField(max_length = 8,choices = [('MALE','MALE'),('FEMALE','FEMALE')])
    city        = models.CharField(max_length=50, help_text='Employee City')
    phone       = models.CharField(max_length=20, help_text='Employee Phone')
    education   = models.TextField(max_length=1000,null=True,blank=True)
    experience  = models.TextField(max_length=1000,null=True,blank=True)
    awards      = models.TextField(max_length=1000,null=True,blank=True)
    hobbies     = models.TextField(max_length=1000,null=True,blank=True)
    skills      = models.TextField(max_length=1000)
    references  = models.TextField(max_length=1000,null=True,blank=True)
    other       = models.TextField(max_length=1000,null=True,blank=True)
    cluster     = models.IntegerField(null=True,blank=True)
    clusterable_text   = models.TextField(null=True,blank=True)
    
    def __str__(self):
        """String for representing the Employee object (in Admin site etc.)."""
        return self.firstname+" "+self.lastname
    
    def get_age(self):
        """function r=to return employee age based on thier birthday"""
        today = date.today()
        birthyear = self.dateOfBirth.year
        age = today.year - birthyear
        # Account for birthdays not yet passed in the current year
        if (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day):
            age -= 1
        return str(age)


class Company(models.Model):

    user  = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name  = models.CharField(max_length=100, help_text='Company Name') 
    city  = models.CharField(max_length=100, help_text='Company City')
    phone = models.CharField(max_length=20, help_text='Company Phone')

    def __str__(self):
        """String for representing the Company object (in Admin site etc.)."""
        return self.name