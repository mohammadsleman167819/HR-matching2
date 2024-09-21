from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import transaction
from .models import Company, Employee, User
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    """class extend UserCreationForm to remove username field and keep only email"""
    class Meta:
        model = User
        fields = ("email","is_employee","is_company")


class CustomUserChangeForm(UserChangeForm):
    """class extend UserCreationForm to remove username field and keep only email"""
    class Meta:
        model = User
        fields = ("email","is_employee","is_company")



class EmployeeSignUpForm(CustomUserCreationForm):
    
    firstname = forms.CharField(label="First Name", max_length=100, help_text='Employee First Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label="Last Name", max_length=100, help_text='Employee Last Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateOfBirth = forms.DateField(label="Date Of Birth", help_text='Employee Date of Birth',
                                  widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date" , 'class': 'form-control'}),
                                    input_formats=["%Y-%m-%d"])
    gender = forms.ChoiceField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], label="Gender",widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=50, help_text='Employee City',widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone", max_length=20,min_length=10, help_text='Employee Phone',widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(label="Education", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    experience = forms.CharField(label="Experience", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    awards = forms.CharField(label="Awards", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    hobbies = forms.CharField(label="Hobbies", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    skills = forms.CharField(label="Skills", max_length=1000,widget=forms.Textarea(attrs={'class': 'form-control'}))
    references = forms.CharField(label="References", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    other = forms.CharField(label="Other", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    
    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data    
    
    def clean_dateOfBirth(self):       
        data = self.cleaned_data["dateOfBirth"]
        birthyear = data.year
        today = date.today()
        age = today.year - birthyear
        if (today.month, today.day) < (data.month, data.day):
            age -= 1 
        if data > today:
            raise ValidationError('Date of birth cannot be in the future.')
        minimum_age = 16 
        maximum_age = 120  
        if age < minimum_age:
            raise ValidationError(f'You must be at least {minimum_age} years old to register.')
        if age > maximum_age:
            raise ValidationError(f'{age} years old is not a valid value.')
        return data

    class Meta(CustomUserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_company = False
        user.save()
        Employee.objects.create(
            user=user,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            dateOfBirth=self.cleaned_data.get('dateOfBirth'),
            gender=self.cleaned_data.get('gender'),
            city=self.cleaned_data.get('city'),
            phone=self.cleaned_data.get('phone'),
            education=self.cleaned_data.get('education'),
            experience=self.cleaned_data.get('experience'),
            awards=self.cleaned_data.get('awards'),
            hobbies=self.cleaned_data.get('hobbies'),
            skills=self.cleaned_data.get('skills'),
            references=self.cleaned_data.get('references'),
            other=self.cleaned_data.get('other')
        )
        return user




class CompanySignUpForm(CustomUserCreationForm):
    
    name  = forms.CharField(label = "Comapany Name", max_length = 100,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    
    city = forms.CharField(label="City", max_length=50,
                           widget = forms.TextInput(attrs={'class': 'form-control'}))
    
    phone = forms.CharField(label="Phone", max_length=20,min_length=10,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    

    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data
 
 
    class Meta(CustomUserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.is_employee = False
        user.save()
        company = Company.objects.create(
            user=user,
            name = self.cleaned_data['name'],
            city= self.cleaned_data['city'],
            phone=self.cleaned_data['phone']
            )
        return user

