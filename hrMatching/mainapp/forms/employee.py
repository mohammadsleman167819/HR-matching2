from django import forms
from django.db import transaction
from ..models import Employee, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .home import CustomUserCreationForm
from django.core.exceptions import ValidationError
from datetime import date


class EmployeeBaseForm(forms.ModelForm):
    """
    Base class for other Employee From to extend

    fields:
        - firstname,lastname,dateOfBirth,gender,city,phone
        - education,experience,awards,hobbies,skills,references,other
    methods:
        clean_phone : make sure phone entered is all digits and '-' or '+'
        add_helper_layout : define a basic layout for crispy forms
        clean_dateOfBirth : make sure age in the range [16,80]
    """

    firstname = forms.CharField(
        label="First Name",
        max_length=100,
        help_text="Employee First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    lastname = forms.CharField(
        label="Last Name",
        max_length=100,
        help_text="Employee Last Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    dateOfBirth = forms.DateField(
        label="Date Of Birth",
        help_text="Employee Date of Birth",
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    gender = forms.ChoiceField(
        choices=[("MALE", "MALE"), ("FEMALE", "FEMALE")],
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        help_text="Employee City",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Phone",
        max_length=20,
        min_length=10,
        help_text="Employee Phone",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    education = forms.CharField(
        label="Education",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    experience = forms.CharField(
        label="Experience",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    awards = forms.CharField(
        label="Awards",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    hobbies = forms.CharField(
        label="Hobbies",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    skills = forms.CharField(
        label="Skills",
        max_length=1000,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    references = forms.CharField(
        label="References",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    other = forms.CharField(
        label="Other",
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        msg = 'Phone number can only contain digits, hyphens, and plus signs.'
        for char in data:
            if not char.isdigit() and char not in "-+":
                raise ValidationError(msg)
        return data

    def clean_dateOfBirth(self):
        data = self.cleaned_data["dateOfBirth"]
        birthyear = data.year
        today = date.today()
        age = today.year - birthyear
        if (today.month, today.day) < (data.month, data.day):
            age -= 1
        if data > today:
            raise ValidationError("Date of birth cannot be in the future.")
        if age < 16:
            raise ValidationError(
                "You must be at least 16 years old to register."
            )
        if age > 80:
            raise ValidationError("Sorry you must be under 80.")
        return data

    class Meta:
        fields = (
            "firstname",
            "lastname",
            "dateOfBirth",
            "gender",
            "city",
            "phone",
            "education",
            "experience",
            "awards",
            "hobbies",
            "skills",
            "references",
            "other",
        )


class EmployeeSignUpForm(CustomUserCreationForm, EmployeeBaseForm):
    """
    SignUp as employee Form_Class

    - extends EmployeeBaseForm
    - alter fields to add User Fields ( email , password)
    - alter Layout to add User Fields ( email , password)

    methods:
        save:
            - set user type flags
            - create company object
            - set OneToOne field with the created user
    """

    class Meta(CustomUserCreationForm.Meta, EmployeeBaseForm.Meta):
        model = User
        user_fields = CustomUserCreationForm.Meta.fields
        employee_fields = EmployeeBaseForm.Meta.fields
        fields = user_fields + employee_fields

    def __init__(self, *args, **kwargs):
        super(EmployeeSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "User Information",
                "email",
                "password1",
                "password2",
            ),
            Fieldset(
                "Personal Information",
                "firstname",
                "lastname",
                "dateOfBirth",
                "gender",
                "city",
                "phone",
            ),
            Fieldset(
                "Professional Information",
                "education",
                "experience",
                "awards",
                "hobbies",
                "skills",
                "references",
                "other",
            ),
            ButtonHolder(Submit("submit", "Sign Up", css_class="btn-primary")),
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_company = False
        user.save()
        Employee.objects.create(
            user=user,
            firstname=self.cleaned_data["firstname"],
            lastname=self.cleaned_data["lastname"],
            dateOfBirth=self.cleaned_data["dateOfBirth"],
            gender=self.cleaned_data["gender"],
            city=self.cleaned_data["city"],
            phone=self.cleaned_data["phone"],
            education=self.cleaned_data["education"],
            experience=self.cleaned_data["experience"],
            awards=self.cleaned_data["awards"],
            hobbies=self.cleaned_data["hobbies"],
            skills=self.cleaned_data["skills"],
            references=self.cleaned_data["references"],
            other=self.cleaned_data["other"],
        )
        return user


class EmployeeUpdateForm(EmployeeBaseForm):
    """Update Employee User info Form_Class ,extends EmployeeBaseForm"""

    class Meta(EmployeeBaseForm.Meta):
        model = Employee

    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                "firstname",
                "lastname",
                "dateOfBirth",
                "gender",
                "city",
                "phone",
            ),
            Fieldset(
                "Professional Information",
                "education",
                "experience",
                "awards",
                "hobbies",
                "skills",
                "references",
                "other",
            ),
            ButtonHolder(Submit("submit", "Save", css_class="btn-primary")),
        )
