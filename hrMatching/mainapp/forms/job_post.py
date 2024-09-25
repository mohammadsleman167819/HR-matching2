from django import forms
from ..models import Job_Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class Job_PostBaseForm(forms.ModelForm):
    """
    Base class for other Job_Post From to extend

    fields:
        job_title, jobDescription 
        workhours, contact, city, salary

    """
    job_title = forms.CharField(
        label="Job Title",
        max_length=350,
        widget = forms.TextInput(attrs={'class': 'form-control'})        
        )
    jobDescription = forms.CharField(
        label="Job Description",
        max_length=5000,
        widget = forms.Textarea(attrs={'class': 'form-control'})
        )
    workhours = forms.CharField(
        label="Work Hours",
        max_length=1000,
        widget = forms.Textarea(attrs={'class': 'form-control'})
        )
    contact = forms.CharField(
        label="Contact",
        max_length=50,
        widget = forms.TextInput(attrs={'class': 'form-control'})
        )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget = forms.TextInput(attrs={'class': 'form-control'})
        )
    salary = forms.CharField(
        label="Salary",
        max_length=50,
        widget = forms.TextInput(attrs={'class': 'form-control'})
        )
    
    class Meta:
        fields = ('job_title', 'jobDescription', 
        'workhours', 'contact', 'city', 'salary')

    def add_helper_layout(self):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Job Post Information',
                'job_title',
                'jobDescription',
                'workhours',
                'contact',
                'city',
                'salary'
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn-primary')
            )
        )


class Job_PostCreateForm(Job_PostBaseForm):
    """Create Job_Post Form_Class, extends Job_PostBaseForm"""
    class Meta(Job_PostBaseForm.Meta):
        model = Job_Post

    def __init__(self, *args, **kwargs):
        super(Job_PostCreateForm, self).__init__(*args, **kwargs)
        self.add_helper_layout()


class Job_PostUpdateForm(Job_PostBaseForm):
    """Update Job_Post Form_Class, extends Job_PostBaseForm"""

    class Meta(Job_PostBaseForm.Meta):
        model = Job_Post

    def __init__(self, *args, **kwargs):
        super(Job_PostUpdateForm, self).__init__(*args, **kwargs)
        self.add_helper_layout()
