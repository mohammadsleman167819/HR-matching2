from django.test import TestCase
from django.urls import resolve, reverse
from . import UrlTests
from ...views import home


class SignUpUrlTests(UrlTests, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "signup"
        cls.url = "accounts/signup/"
        cls.template = "registration/signup.html"
        cls.view_class = home.SignUpView
        cls.view_func = None
        cls.args = {}


class indexUrlTests(UrlTests, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "index"
        cls.url = ""
        cls.template = "mainapp/index.html"
        cls.view_func = home.index
        cls.view_class = None
        cls.args = {}


class loginUrlTests(UrlTests, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "login"
        cls.url = "accounts/login"
        cls.template = "registration/login.html"
        cls.view_class = home.LoginView
        cls.view_func = None
        cls.args = {}
