from django.shortcuts import redirect,reverse,render
from django.views.generic import CreateView,UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from ..models import User,Employee,Company
from django.contrib.auth import login

__all__ = [
    'redirect',
    'reverse',
    'CreateView',
    'UpdateView',
    'DetailView',
    'LoginRequiredMixin',
    'User',
    'Employee',
    'Company',
    'login',
    'UserPassesTestMixin','render'
]