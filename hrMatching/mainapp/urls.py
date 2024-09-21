from django.urls import path,include
from .views import home,company,employee
urlpatterns = [
    path('', home.index, name='index'),
    path('company/<int:pk>/update/<int:changed>',company.CompanyUpdateView.as_view(),name='company_update'),
   # path('/employee/myprofile',employee.EmployeeUpdateView,name='employee_update')
]
