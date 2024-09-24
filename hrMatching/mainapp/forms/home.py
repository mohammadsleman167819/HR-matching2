from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    """Extends UserCreationForm to remove username field and keep only email"""

    class Meta:
        model = User
        fields = ("email", "is_employee", "is_company")


class CustomUserChangeForm(UserChangeForm):
    """Extends UserCreationForm to remove username field and keep only email"""

    class Meta:
        model = User
        fields = ("email", "is_employee", "is_company")


class CustomLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ("email", "password1")

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset("Log in", "email", "password1"),
        )
