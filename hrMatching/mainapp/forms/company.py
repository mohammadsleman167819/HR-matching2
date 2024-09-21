from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import transaction
from ..models import Company,User
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .home import CustomUserCreationForm

 
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
        fields = ('email','password1','password2','name','city','phone')

    def __init__(self,*args,**kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User Information',
                'email',
                'password1',
                'password2',
            ),
            Fieldset(
                'Company Information',
                'name',
                'city',
                'phone',
            ),
            ButtonHolder(
                Submit('submit', 'Sign Up', css_class='btn-primary')
            )
        )


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

