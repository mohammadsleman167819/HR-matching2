
from django.contrib import admin
from django.urls import path,include
from mainapp.views import home,company,employee
urlpatterns = [
    path('',include('mainapp.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/signup/',home.SignUpView.as_view(),name='signup'),
    path('accounts/signup/employee',employee.EmployeeSignUpView.as_view(),name='employee_signup'),
    path('accounts/signup/company',company.CompanySignUpView.as_view(),name='company_signup'),
    path("admin/", admin.site.urls),
]
