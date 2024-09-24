from django import forms
from django.db import transaction
from ..models import Company, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .home import CustomUserCreationForm
from django.core.exceptions import ValidationError


class CompanyBaseForm(forms.ModelForm):
    """
    Base class for other Company From to extend

    fields:
        name,city,phone

    methods:
        clean_phone : make sure phone entered is all digits and '-' or '+'
        add_helper_layout : define a basic layout for crispy forms
    """

    name = forms.CharField(
        label="Company Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        label="Phone",
        max_length=20,
        min_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_phone(self):
        data = self.cleaned_data['phone']
        msg = 'Phone number can only contain digits, hyphens, and plus signs.'
        for char in data:
            if not char.isdigit() and char not in '-+':
                raise ValidationError(msg)
        return data

    class Meta:
        fields = ('name', 'city', 'phone')

    def add_helper_layout(self):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Company Information',
                'name',
                'city',
                'phone',
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn-primary')
            )
        )


class CompanySignUpForm(CustomUserCreationForm, CompanyBaseForm):
    """
        SignUp as Company Form class

        - extends CompanyBaseForm
        - alter fields to add User Fields ( email , password)
        - alter Layout to add User Fields ( email , password)

        methods:
            save:
                - set user type flags
                - create company object
                - set OneToOne field with the created user
    """

    class Meta(CustomUserCreationForm.Meta, CompanyBaseForm.Meta):
        model = User
        user_fields = CustomUserCreationForm.Meta.fields
        company_fields = CompanyBaseForm.Meta.fields
        fields = user_fields + company_fields

    def __init__(self, *args, **kwargs):
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
        Company.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            city=self.cleaned_data['city'],
            phone=self.cleaned_data['phone']
        )
        return user


class CompanyUpdateForm(CompanyBaseForm):
    """Update Company User info Form_Class, extends CompanyBaseForm"""

    class Meta(CompanyBaseForm.Meta):
        model = Company

    def __init__(self, *args, **kwargs):
        super(CompanyUpdateForm, self).__init__(*args, **kwargs)
        self.add_helper_layout()
