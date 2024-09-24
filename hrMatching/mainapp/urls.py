from django.urls import path, include
from .views import home, company, employee

urlpatterns = [
    path("", home.index, name="index"),
]

urlpatterns += [
    path(
        "employee/<int:pk>/update/<int:changed>",
        employee.EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employee/<int:pk>/details",
        employee.EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
]

urlpatterns += [
    path(
        "company/<int:pk>/update/<int:changed>",
        company.CompanyUpdateView.as_view(),
        name="company_update",
    ),
    path(
        "company/<int:pk>/details",
        company.CompanyDetailView.as_view(),
        name="company_detail",
    ),
]
