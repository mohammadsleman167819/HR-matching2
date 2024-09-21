from django.urls import path,include
from .views import home,company,employee
urlpatterns = [
    path('', home.index, name='index'),
]
