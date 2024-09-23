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
     - added flags to show the user type (employee/company)
    
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
    """
    Employee model handle users of type employee
    
    Has the following attributes:
        user : OneToOneField with User instance , primary key
        personal information stored in CharFields (required): 
            (firstname , lastname , dateOfBirth , gender , city , phone)
        professional information stored in TextFields (only skill required):
            (education ,  experience,   awards ,   hobbies ,   skills ,   references,  other)       
        machine learning model related information (set by the model):
            cluster - IntegerField to store the cluster number employee belong to-
            clusterable_text - TextField to store the important imformation for the model all in one string after preprocessing it-
    
    methods:
        __str__ : return firstname + lastname to represent inctanse
        get_age : calculate the employee age based on dateofbirth
        get_absolute_url : return url link to employee detail page
        get_fields : return fields we want to show in employee detail page
    """
    
    
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname   = models.CharField("First Name",max_length=100, help_text='Employee First Name')
    lastname    = models.CharField("Last Name",max_length=100, help_text='Employee Last Name')
    dateOfBirth = models.DateField("Date Of Birth",help_text='Employee Date of Birth')
    gender      = models.CharField("Gender",max_length = 8,choices = [('MALE','MALE'),('FEMALE','FEMALE')])
    city        = models.CharField("City",max_length=50, help_text='Employee City')
    phone       = models.CharField("Phone",max_length=20, help_text='Employee Phone')
    education   = models.TextField("Education",max_length=1000,null=True,blank=True)
    experience  = models.TextField("Experience",max_length=1000,null=True,blank=True)
    awards      = models.TextField("Awards",max_length=1000,null=True,blank=True)
    hobbies     = models.TextField("Hobbies",max_length=1000,null=True,blank=True)
    skills      = models.TextField("Skills",max_length=1000)
    references  = models.TextField("References",max_length=1000,null=True,blank=True)
    other       = models.TextField("Other",max_length=1000,null=True,blank=True)
    cluster     = models.IntegerField("Cluster",null=True,blank=True)
    clusterable_text   = models.TextField("Clusterable Text",null=True,blank=True)

    def __str__(self):
        """String for representing the Employee object (in Admin site etc.)."""
        return self.firstname+" "+self.lastname
    
    def get_age(self):
        """function return employee age based on thier birthday"""
        today = date.today()
        birthyear = self.dateOfBirth.year
        age = today.year - birthyear
        # Account for birthdays not yet passed in the current year
        if (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day):
            age -= 1
        return str(age)
    
    def get_absolute_url(self):
        """Return url to page shows employee details"""
        return reverse('employee_detail', kwargs={'pk': self.pk})

    def get_fields(self):
        """return info to be showed in employee details page"""
        fields = []
        for field in self._meta.fields:
            if field.verbose_name not in ['user','Clusterable Text','Cluster','Date Of Birth']:
                val = field.value_from_object(self)
                if val is None:
                    val = ""
                info =  (field.verbose_name,val)
                fields.append(info)
            if field.verbose_name in ['Date Of Birth']:
                info = ('Age' , self.get_age())
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
        get_fields : return fields (name,value) we want to show in company detail page
    """

    user  = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name  = models.CharField('Name',max_length=100, help_text='Company Name') 
    city  = models.CharField('City',max_length=100, help_text='Company City')
    phone = models.CharField('Phone',max_length=20, help_text='Company Phone')

    def __str__(self):
        """String for representing the Company object (in Admin site etc.)."""
        return self.name
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        
    def get_absolute_url(self):
        """Return url to page shows employee details"""
        return reverse('company_detail', kwargs={'pk': self.pk})

    def get_fields(self):
        """return fields (name,value) we want to show in company detail page"""
        return [
        (field.verbose_name, field.value_from_object(self))
            for field in self._meta.fields
            if field.verbose_name not in ['user']
    ]